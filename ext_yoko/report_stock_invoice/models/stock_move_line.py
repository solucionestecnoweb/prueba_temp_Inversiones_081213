# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    invoice_ids = fields.Many2many(compute="_compute_picking_invoice_ids", comodel_name="account.move",
                                    copy=False, string="Facturas", store=True)
    is_invoice = fields.Boolean(string="Tiene Factura", compute="_compute_picking_invoice_ids", store=True, default=False)

    @api.depends('sale_id.invoice_ids')
    def _compute_picking_invoice_ids(self):
        for picking in self:
            if picking.sale_id.invoice_ids:
                picking.invoice_ids = picking.sale_id.invoice_ids
                picking.is_invoice = True
            else:
                picking.is_invoice = False
                return ''


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    doc_invoice = fields.Char(string="Factura", readonly=True, compute='compute_invoice_and_delivery_note', store=True)
    doc_note_entrega = fields.Char(string="Nota de entrega", readonly=True, compute='compute_invoice_and_delivery_note', store=True)

    @api.depends(
        'picking_id.is_invoice',
        'picking_id.invoice_ids.correlativo_nota_entrega',
        'picking_id.invoice_ids.invoice_number_cli'
    )
    def compute_invoice_and_delivery_note(self):
        for line in self:
            account = line.env['account.move'].search([('invoice_origin', '=', line.origin)])
            if account:
                name = ''
                note = ''
                for move in account:
                    if move.correlativo_nota_entrega:
                        note += move.correlativo_nota_entrega +" "
                    if move.invoice_number_cli:
                        name += move.invoice_number_cli +" "
                line.doc_invoice = name
                line.doc_note_entrega = note
            else:
                line.doc_invoice = ''
                line.doc_note_entrega = ''

