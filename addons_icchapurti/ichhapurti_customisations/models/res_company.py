# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_warehouse = fields.Boolean(string="Warehouse", default=False)
    name_temp = fields.Char()

    @api.onchange('is_warehouse')
    def rename_company(self):
        if self.name:
            if self.is_warehouse:
                self.name_temp = self.name
                self.name = self.name + " ( Warehouse )"
                self.partner_id.is_warehouse = True
            else:
                self.name = self.name_temp
