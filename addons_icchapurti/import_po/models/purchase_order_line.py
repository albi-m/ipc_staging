# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    case_size = fields.Float(string="Case Size")
    barcode = fields.Char(related='product_id.barcode')

