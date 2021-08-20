# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SyncSaleOrder(models.Model):
    """
    Generate a draft purchase order when a company confirms a sales order
    for the current company
    """
    _inherit = 'sale.order'

    sync_order = fields.Boolean(default=False)
    warehouse_id = fields.Many2one(readonly=False)

    def _prepare_invoice(self):
        res = super(SyncSaleOrder, self)._prepare_invoice()
        trans_enabled = self.env['ir.config_parameter'].sudo().get_param(
            'inter_comp_transactions.sale_purchase_sync')
        if trans_enabled and self.partner_id.company_type == 'company':
            res['related_so'] = self.id
        return res

    def action_cancel(self):
        res = super(SyncSaleOrder, self).action_cancel()
        purchase_order = self.env['purchase.order'].sudo().search(
            [('counterpart_so', '=', self.name)])
        for order in purchase_order:
            order.sudo().button_cancel()
        return res
