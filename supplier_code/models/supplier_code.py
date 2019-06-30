# -*- coding: utf-8 -*-

from odoo import api, fields, models
class SaleOrderLine(models.Model):
	_inherit = 'res.partner'

	code = fields.Char(string="Code")




