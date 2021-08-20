# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.onchange('quantity_done')
    def _onchange_quantity_done(self):
        if self.quantity_done > self.product_uom_qty:
            raise ValidationError("Done quantity should be less than or equal to Demand Quantity")


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    qty_done = fields.Float(readonly=True)
