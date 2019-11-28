# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountInvoiceInherit(models.Model):
	_inherit = 'account.invoice'

	from_sale = fields.Boolean('Created From Sale')
	sale_ids =  fields.Many2many('sale.order',string ='Sales')

	def _get_sales_details(self):
		for inv in self:
			if inv.origin and  ',' in inv.origin:
				ref = inv.origin.split(', ')
				sales = []
				for i in ref:
					so = self.env['sale.order'].search([('name','=',i)])
					if so:
						sales.append(so.id)
				if sales:
					inv.write({
						'sale_ids' : [(6,0,sales)],
						'from_sale':True,
						})
				return True		


