# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        sale_order = self.env['sale.order'].sudo().search(
            [('name', '=', self.origin)])
        if sale_order:
            sale_order.check_picking_status()
        return res


class BackorderWizard(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process(self):
        res = super(BackorderWizard, self).process()
        sale_order = self.env['sale.order'].sudo().search(
            [('name', '=', self.pick_ids.origin)])
        if sale_order:
            sale_order.custom_state = 'picking_partial'
        return res