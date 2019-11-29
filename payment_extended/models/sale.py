# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line')
    def _total_payment(self):
    	if self.order_line:
    		self.tot_cash = sum(self.mapped('order_line.cash'))
    		self.tot_credit_card = sum(self.mapped('order_line.credit_card'))
    		self.tot_voucher = sum(self.mapped('order_line.voucher'))
    		self.tot_mobile = sum(self.mapped('order_line.mobile'))
    		self.tot_eft = sum(self.mapped('order_line.eft'))

    tot_cash = fields.Float(compute='_total_payment', string='Total Cash', readonly=True)
    tot_credit_card = fields.Float(compute='_total_payment', string='Total Credit', readonly=True)
    tot_voucher = fields.Float(compute='_total_payment', string='Total Voucher', readonly=True)
    tot_mobile = fields.Float(compute='_total_payment', string='Total Mobile', readonly=True)
    tot_eft = fields.Float(compute='_total_payment', string='Total Eft', readonly=True)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    cash = fields.Float("Cash")
    credit_card = fields.Float("Bank")
    voucher = fields.Float("voucher")
    mobile = fields.Float("Mobile")
    eft = fields.Float("EFT")


    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if res:
            res.update({
            	'cash': self.cash,
            	'credit_card': self.credit_card,
            	'voucher': self.voucher,
            	'mobile':self.mobile,
            	'eft': self.eft,
            	})
        return res