# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfig(models.TransientModel):
    """
    Adding option to enable the sale/purchase order sync
    """
    _inherit = 'res.config.settings'

    sale_purchase_sync = fields.Boolean(string="Synchronize Sales and Purchase Order",
                                        config_parameter='inter_comp_transactions.sale_purchase_sync')
    auto_validate = fields.Boolean(string="Auto confirm orders",
                                   config_parameter='inter_comp_transactions.auto_validate')
