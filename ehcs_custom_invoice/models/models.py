# -*- coding: utf-8 -*-

from odoo import models, fields, api

class invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _get_computed_reference(self):
    	return self.number
