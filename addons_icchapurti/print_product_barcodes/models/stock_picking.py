# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models,fields,api
import math


class StockMoveLines(models.Model):
    _inherit = "stock.move.line"

    # returns the ceiled value for box count
    def _get_box_count(self):
        box_count = 0
        for line in self:
            if line.product_id.case_size:
                box_count = math.ceil(line.qty_done/line.product_id.case_size)
            else:
                box_count = line.qty_done
        return int(box_count)


class StockPackages(models.Model):
    _inherit = "stock.quant.package"

    def _get_picking(self):
        domain = ['|', ('result_package_id', 'in', self.ids), ('package_id', 'in', self.ids)]
        pickings = self.env['stock.move.line'].search(domain).mapped('picking_id')
        return pickings[0]
