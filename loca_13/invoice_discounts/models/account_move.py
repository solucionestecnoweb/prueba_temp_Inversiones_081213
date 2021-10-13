# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_discount = fields.Boolean(string='Tiene Descuento')
    discount5 = fields.Float(string="Descuento 1")
    discount3 = fields.Float(string="Descuento 2")
    discount2 = fields.Float(string="Descuento 3")

    @api.onchange('discount5')
    def _onchange_discount5_invoice(self):
        if self.discount5 > 0:
            disc5 = (self.amount_total * self.discount5) / 100
            self.amount_total = disc5

    @api.onchange('discount3')
    def _onchange_discount3_invoice(self):
        if self.discount3 > 0:
            disc3 = (self.amount_total * self.discount3) / 100
            self.amount_total = disc3

    @api.onchange('discount2')
    def _onchange_discount2_invoice(self):
        if self.discount3 > 0:
            disc2 = (self.amount_total * self.discount2) / 100
            self.amount_total = disc2