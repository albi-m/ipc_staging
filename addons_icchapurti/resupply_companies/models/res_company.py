# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _compute_same_company(self):
        for rec in self:
            rec.is_same_company = False
            if rec.id == self.env.company.id:
                rec.is_same_company = True

    resupply_company = fields.Many2one('res.company', string="Resupply company",
                                       readonly=False,
                                       domain=[('company_type', '=', 'warehouse')])
    company_type = fields.Selection(selection=[
        ('warehouse', 'Warehouse'), ('bp', 'BP')], default='bp', required=True)
    is_same_company = fields.Boolean(compute=_compute_same_company)

    def apply_resupply_company(self):
        vals = {
            'name': self.resupply_company.partner_id.id,
        }
        print(vals)
        products = self.env['product.template'].search([]).write({
            'seller_ids': [(0, 0, vals)]
        })

    @api.onchange('company_type')
    def rename_company(self):
        print("-------------")
        if self.name:
            if self.company_type == 'warehouse':
                self.name_temp = self.name
                self.name = self.name + " ( Warehouse )"
                self.partner_id.is_warehouse = True
            else:
                self.name = self.name_temp
