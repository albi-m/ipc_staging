# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    user_assign_companies = fields.Selection(selection=[
        ('warehouse', 'Warehouse'), ('bp', 'BP')], string="Type of company")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.onchange('user_assign_companies')
    def assign_companies(self):
        if self.user_assign_companies == 'warehouse':
            company_ids = self.env['res.company'].search(
                [('company_type', '=', 'warehouse')]).ids
            company_ids.append(self.env.company.id)
            self.company_ids = company_ids
        elif self.user_assign_companies == 'bp':
            company_ids = self.env['res.company'].search(
                [('company_type', '=', 'bp')]).ids
            company_ids.append(self.env.company.id)
            self.company_ids = company_ids
        else:
            self.company_ids = False
