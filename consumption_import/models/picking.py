# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
import tempfile
import binascii
import xlrd
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
from collections import namedtuple

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)
import io

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

#class AccountMove(models.Model):
#    _inherit = "account.move"
#
#    @api.multi
#    def post(self):
#        invoice = self._context.get('invoice', False)
#        self._post_validate()
#
#        for move in self:
#            move.line_ids.create_analytic_lines()
#            if move.name == '/':
#                new_name = False
#                journal = move.journal_id
#
#                if invoice and invoice.move_name and invoice.move_name != '/':
#                    new_name = invoice.move_name
#                elif invoice and invoice.custom_seq :
#                    new_name = invoice.name
#                elif invoice and invoice.system_seq :
#                    new_name = invoice.name
#                else:
#                    if journal.sequence_id:
#                        # If invoice is actually refund and journal has a refund_sequence then use that one or use the regular one
#                        sequence = journal.sequence_id
#                        if invoice and invoice.type in ['out_refund', 'in_refund'] and journal.refund_sequence:
#                            sequence = journal.refund_sequence_id
#                        new_name = sequence.with_context(ir_sequence_date=move.date).next_by_id()
#                    else:
#                        raise UserError(_('Please define a sequence on the journal.'))
#
#                if new_name:
#                    move.name = new_name
#        return self.write({'state': 'posted'})


#class account_invoice(models.Model):
#    _inherit = 'account.invoice'
#
#    custom_seq = fields.Boolean('Custom Sequence')
#    system_seq = fields.Boolean('System Sequence')


class import_pickingss(models.TransientModel):
    _name = "import.picking"

    file = fields.Binary('File')
#    type = fields.Selection([('incoming', 'Incoming Shipment'), ('delivery', 'Delivery Orders')], string='Type', required=True, default='incoming')
#    sequence_opt = fields.Selection([('custom', 'Use Excel/CSV Sequence Number'), ('system', 'Use System Default Sequence Number')], string='Sequence Option',default='custom')
    import_option = fields.Selection([('csv', 'CSV File'),('xls', 'XLS File')],string='Select',default='csv')
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type')
    location_id = fields.Many2one(
        'stock.location', "Source Location Zone",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_src_id,
        required=True,
        )
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location Zone",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
        required=True,
        )
    picking_type_code = fields.Selection([
        ('incoming', 'Vendors'),
        ('outgoing', 'Customers'),
        ('internal', 'Internal')], related='picking_type_id.code')
    #import_prod_option = fields.Selection([('barcode', 'Barcode'),('code', 'Code'),('name', 'Name')],string='Import Product By ',default='name')
    import_prod_option = fields.Selection([('barcode', 'Barcode'),('name', 'Name')],string='Import Product By ',default='name')


#
    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):
        res = {}
        if not self.picking_type_id:
            return res
        self.location_id = self.picking_type_id.default_location_src_id.id
        self.location_dest_id = self.picking_type_id.default_location_dest_id.id
        
    @api.multi
    def create_picking(self, values):
        picking_obj = self.env['stock.picking']
        picking_search = picking_obj.search([('id', '=', values.get('last_id'))])
        #picking_search = picking_obj.search([],order='id desc', limit=1)
        print("============")
        print(picking_search)
        print("============")
        pick_id = False 
        if picking_search:
            pick_id = picking_search[0]
            lines = self.make_picking_line(values, picking_search)
            return lines
        else:
            #partner_id = self.find_partner(values.get('customer'))
            pick_date = self._get_date(values.get('date'))
            pick_id = picking_obj.create({
                                         #'name' : values.get('name'),
                                        #'partner_id' : partner_id.id,
                                        'scheduled_date' : pick_date,
                                        'picking_type_id': values.get('picking_type_id'),
                                        'location_id':values.get('location_id'),
                                        'location_dest_id':values.get('location_dest_id'),
                                        'origin' : values.get('origin'),
                                        })
            lines = self.make_picking_line(values, pick_id)
        return pick_id

    @api.multi
    def make_picking_line(self, values, pick_id):
        product_obj = self.env['product.product']
        stock_lot_obj = self.env['stock.production.lot']
        stock_move_obj = self.env['stock.move']
        stock_move_line_obj = self.env['stock.move.line']
        if self.import_prod_option == 'barcode':
            product_id=product_obj.search([('barcode',  '=',values.get('product'))])
        elif self.import_prod_option == 'code':
            product_id=product_obj.search([('default_code', '=',values.get('product'))])
        else:
            product_id=product_obj.search([('name', '=',values.get('product'))])
        #if values.get('lot'):
        #   lot_id=stock_lot_obj.search([('name','=',values.get('lot'))])
     
        if not product_id:
            raise Warning(_('Product is not available "%s" .') % values.get('product'))

        #if not lot_id:
        #    raise Warning(_('Product Lot is not available "%s" .') % values.get('lot'))
        #if lot_id:
        res = stock_move_obj.create({
                'product_id' : product_id.id,
                'name':product_id.name,
                'product_uom_qty' : values.get('quantity'),
                'picking_id':pick_id.id,
                'location_id':pick_id.location_id.id,
                'date_expected':pick_id.scheduled_date,
                'location_dest_id':pick_id.location_dest_id.id,
                'product_uom':product_id.uom_id.id,})


        # res = stock_move_line_obj.create({'location_id':pick_id.location_id.id,
        #                                 'location_dest_id':pick_id.location_dest_id.id,
        #                               'qty_done':values.get('quantity'),
        #                             'product_id': product_id.id,
        #                              'move_id':res.id,
        #                             #'lot_id':lot_id.id,
        #                            'product_uom_qty':values.get('quantity'),
        #                          'product_uom_id':product_id.uom_id.id,}
        #         )
        # else:
        #     res = stock_move_obj.create({
        #         'product_id' : product_id.id,
        #         'name':product_id.name,
        #         'product_uom_qty' : values.get('quantity'),
        #         'picking_id':pick_id.id,
        #         'location_id':pick_id.location_id.id,
        #         'date_expected':pick_id.scheduled_date,
        #         'location_dest_id':pick_id.location_dest_id.id,
        #         'product_uom':product_id.uom_id.id,
            
        #         })
        return True

    @api.multi
    def find_partner(self, name):
        partner_obj = self.env['res.partner']
        partner_search = partner_obj.search([('name', '=', name)])
        if partner_search:
            return partner_search
        else:
            partner_id = partner_obj.create({
                                             'name' : name})
            return partner_id
    
    @api.multi
    def _get_date(self, date):
        DATETIME_FORMAT = "%Y-%m-%d"
        i_date = datetime.strptime(date, DATETIME_FORMAT)
        return i_date

    @api.multi
    def import_picking(self):
        if not self.file:
            raise Warning(_("Please select a file first then proceed"))
        if self.import_option == 'csv':
            #keys = ['name', 'customer', 'origin', 'date', 'product', 'quantity','lot']
            keys = ['origin', 'date', 'product', 'quantity']	 				
            data = base64.b64decode(self.file)
            file_input = io.StringIO(data.decode("utf-8"))
            file_input.seek(0)
            reader_info = []
            reader = csv.reader(file_input, delimiter=',')
 
            try:
                reader_info.extend(reader)
                print(reader_info)
            except Exception:
                raise exceptions.Warning(_("Not a valid file!"))
            values = {}
            picking_ids=[]
            last_id = self.env['stock.picking'].search([],order='id desc', limit=1).id
            last_id = last_id + 1 

            for i in range(len(reader_info)):
	            field = map(str, reader_info[i])
	            values = dict(zip(keys, field))
	            if values:
                     
	                if i == 0:
	                    continue
	                else:
	                    values.update({'picking_type_id':self.picking_type_id.id,
                                    'location_id':self.location_id.id,
                                    'location_dest_id':self.location_dest_id.id,
                                    'last_id': last_id})
	                    res = self.create_picking(values)
        else: 
            fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            if not workbook:
                raise UserError(_("Cannot find file"))
            sheet = workbook.sheet_by_index(0)
            picking_ids=[]
            last_id = self.env['stock.picking'].search([],order='id desc', limit=1).id
            last_id = last_id + 1 
            for row_no in range(sheet.nrows):

                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    
                    line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    a1 = int(float(line[1]))
                    a1_as_datetime = datetime(*xlrd.xldate_as_tuple(a1, workbook.datemode))
                    date_string = a1_as_datetime.date().strftime('%Y-%m-%d')
                    values.update( {
                                    #'name': line[0],
									#'customer': line[0],
									'origin':line[0],
                                    'product': line[2],
									'quantity': line[3],
                                    'date': date_string,
                                    'picking_type_id':self.picking_type_id.id,
                                    'location_id':self.location_id.id,
                                    'location_dest_id':self.location_dest_id.id,
                                    'last_id': last_id
                                    #'lot':line[6].split('.')[0]
						
                                    })
                    res = self.create_picking(values)

