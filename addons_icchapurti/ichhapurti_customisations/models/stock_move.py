# -*- coding: utf-8 -*-

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_available_qty(self):
        for rec in self:
            rec.available_reserved_qty = 1
            stock_quant = self.env['stock.quant'].search(
                [('location_id', '=', rec.picking_id.location_id.id),
                 ('product_id', '=', rec.product_id.id)])
            if stock_quant:
                rec.available_reserved_qty = stock_quant.available_quantity
            else:
                rec.available_reserved_qty = 0
            print(rec.available_reserved_qty)

    available_reserved_qty = fields.Float(string="Available Quantity",
                                          compute=_get_available_qty)
