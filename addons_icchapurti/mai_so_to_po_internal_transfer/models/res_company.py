# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    # po_from_so = fields.Boolean('Create Purchase Orders when selling to this company')
    po_option = fields.Selection([('sale', 'Sale Confirm'), ('invoice', 'Invoice Confirm')], 'Create Purchase Orders Option', default='invoice',)
    po_company_id = fields.Many2one('res.company', 'Purchase Company')
