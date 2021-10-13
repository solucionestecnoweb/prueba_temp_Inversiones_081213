# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models,api,_
import datetime
from odoo.exceptions import UserError, ValidationError

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost.lines'

    price_unit_aux = fields.Float()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_secundaria_id.id)

    @api.onchange('price_unit_aux','currency_id')
    #@api.depends('price_unit_aux','currency_id')
    def calcula_tasa(self):
        for selff in self:
            if selff.env.company.currency_id.id==selff.currency_id.id:
                pass
                selff.price_unit=selff.price_unit_aux
            else:
                lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', selff.currency_id.id),('hora','<=',selff.cost_id.date)],order='hora ASC')
                if lista_tasa:
                    for det in lista_tasa:
                        valor=selff.price_unit_aux/det.rate
                    selff.price_unit=valor


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    line_resumen  = fields.Many2many(comodel_name='stock.landed.resumen', string='Lineas')


    def _compute_monto_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            if self.env.company.currency_secundaria_id.id==selff.currency_id.id:
                valor=selff.amount_total
            if self.env.company.currency_id.id==selff.currency_id.id:
                lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('name','<=',selff.date)],order='id ASC')
                if lista_tasa:
                    for det in lista_tasa:
                        valor=selff.amount_total_signed*det.rate
            selff.amount_total_signed_aux_bs=valor
            selff.amount_total_signed_bs=valor



    def compute_landed_cost(self):
        super().compute_landed_cost()
        total_cos_dest=self.amount_total
        self.env['stock.landed.resumen'].search([]).unlink()#costo_id
        for det in self.valuation_adjustment_lines:
            self.calculo_nuevo_cost_uni(det.product_id,total_cos_dest)
            #raise UserError(_('Hola pipi padd=%s')%nuevo_costo_unit)

    def calculo_nuevo_cost_uni(self,producto,total_cos_dest):
        if producto.categ_id.property_cost_method=="fifo":
            busca=self.env['stock.valuation.adjustment.lines'].search([('product_id','=',producto.id),('cost_id','=',self.id)])#costo_id
            #raise UserError(_('Hola pipi paaad '))
            if busca:
                costo_adicional=0
                for det in busca:
                    moneda=self.busca_moneda(det.move_id.origin)
                    moneda_compania=self.busca_moneda_company(det.move_id.origin)
                    costo_original_total=det.former_cost
                    costo_adicional=costo_adicional+det.additional_landed_cost
                    cantidad=det.quantity
                    if producto.tasa_compra>0:
                        tasa=producto.tasa_compra
                    else:
                        raise UserError(_('El producto %s no tiene tasa registrada en su compra. Vaya a la ficha del producto y coloque la ultima tasa de compra de éste')%producto.name)
                self.registra_resumen(producto,det,costo_adicional)
                self.line_resumen=self.env['stock.landed.resumen'].search([('cost_id','=',self.id)])#costo_id
                monto_unit_total=((costo_original_total+costo_adicional)/cantidad)
                if producto.standard_price<monto_unit_total:
                    if moneda==moneda_compania:
                        producto.standard_price=monto_unit_total
                        producto.standard_price_div=monto_unit_total/tasa
                    else:
                        producto.standard_price=monto_unit_total#*tasa
                        producto.standard_price_div=monto_unit_total/tasa

    def monto_tasa(self):
        valor=0
        #self.amount_total_signed_aux_bs=valor
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date_approve)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=det.rate
        return valor

    def busca_moneda(self,origen):
        busca=self.env['purchase.order'].search([('name','=',origen)])
        if busca:
            for det in busca:
                moneda=det.currency_id.id
        return moneda

    def busca_moneda_company(self,origen):
        busca=self.env['purchase.order'].search([('name','=',origen)])
        if busca:
            for det in busca:
                moneda_company=det.company_id.currency_id.id
        return moneda_company

    def registra_resumen(self,producto,det,costo_adicional):
        #raise UserError(_('Hola pipi paaad '))
        valida=self.env['stock.landed.resumen'].search([('product_id','=',producto.id),('cost_id','=',self.id)]) #('cost_id','=',self.id)
        if not valida:
            if not producto.tasa_compra:
                tasa=1
            else:
                tasa=producto.tasa_compra
            resumen=self.env['stock.landed.resumen']
            vals = {
                'cost_id': self.id,
                'product_id': producto.id,
                'descripcion':producto.name,
                'cantidad':det.quantity,
                'costo_original':det.former_cost,
                'costo_adicional':costo_adicional,
                'costo_total':(det.former_cost+costo_adicional),
                'costo_unit_new':(det.former_cost+costo_adicional)/det.quantity,
                'costo_unit_new_div':((det.former_cost+costo_adicional)/det.quantity)/tasa,
            }
            self.line_resumen = resumen.create(vals)


        #raise UserError(_('Hola pipi paaad 2=%s')%busca)

class StockLandedResumen(models.Model):
    _name = 'stock.landed.resumen'

    cost_id=fields.Many2one('stock.landed.cost', 'Currency')
    product_id=fields.Many2one('product_template')
    descripcion=fields.Char()
    cantidad=fields.Float()
    costo_original=fields.Float()
    costo_adicional=fields.Float()
    costo_total=fields.Float()
    costo_unit_new=fields.Float()
    costo_unit_new_div=fields.Float()
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id.id)
    currency_company_id=fields.Many2one('res.currency',default=lambda self: self.env.company.currency_id.id)
    currency_company_secundaria_id=fields.Many2one('res.currency',default=lambda self: self.env.company.currency_secundaria_id.id)

