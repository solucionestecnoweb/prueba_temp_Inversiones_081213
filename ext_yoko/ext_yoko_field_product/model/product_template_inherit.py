# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class Productos(models.Model):
    _inherit = 'product.template'

    sublineas=fields.Char(string="Sub Lineas")
    #modelo_id = fields.Many2one('stock.modelo')
    modelo_id = fields.Char()
    #tipo_id = fields.Many2one('stock.tipo')
    tipo_id = fields.Char()
    forma_id = fields.Char('stock.forma')
    #forma_id = fields.Many2one('stock.forma')
    color=fields.Char(string="Color")
    formato=fields.Char(string="Formato")
    uso=fields.Char(string="Uso")
    material=fields.Char(string="Material")
    marca_comercial=fields.Char(string="Marca Comercial")
    calidad=fields.Char(string="Calidad")
    uni_neg_id = fields.Char()
    #uni_neg_id = fields.Many2one('stock.unidad.negocio')

class ModeloStock(models.Model):
    _name = 'stock.modelo'

    name=fields.Char()

class TipoStock(models.Model):
    _name = 'stock.tipo'

    name=fields.Char()

class TipoStock(models.Model):
    _name = 'stock.forma'

    name=fields.Char()

class UnidadNegocioStock(models.Model):
    _name = 'stock.unidad.negocio'

    name=fields.Char()
        