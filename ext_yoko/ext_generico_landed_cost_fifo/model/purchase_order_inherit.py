# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models,api,_
import datetime
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        super().button_confirm()
        #raise UserError(_('Hola pipi padd=%s')%tasa)
        tasa=(1/self.currency_rate)
        moneda=self.currency_id.id
        moneda_compania=self.company_id.currency_id.id
        for det_line in self.order_line:
            #metodo_costo=det_line.product_id.product_tmpl_id.categ_id.property_cost_method
            metodo_costo=det_line.product_id.categ_id.property_cost_method
            valor_costo_unitario=det_line.price_unit
            if metodo_costo=="fifo":
                if moneda==moneda_compania:
                    if valor_costo_unitario>det_line.product_id.standard_price:
                        det_line.product_id.standard_price=valor_costo_unitario
                        det_line.product_id.tasa_compra=(1/self.monto_conversion())#tasa
                        det_line.product_id.standard_price_div=valor_costo_unitario*self.monto_conversion()
                else:
                    if (valor_costo_unitario*tasa)>det_line.product_id.standard_price:
                        det_line.product_id.standard_price=valor_costo_unitario*tasa
                        det_line.product_id.tasa_compra=tasa
                        det_line.product_id.standard_price_div=valor_costo_unitario
            #raise UserError(_('producto=%s')%metodo_costo)

    def monto_conversion(self):
        valor=0
        #self.amount_total_signed_aux_bs=valor
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date_approve)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=det.rate
        return valor
