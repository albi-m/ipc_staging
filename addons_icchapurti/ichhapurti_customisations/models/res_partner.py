# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    renamed = fields.Boolean(default=False, store=True)
    rename_text = fields.Char(store=True, default="Company")
    is_warehouse = fields.Boolean(default=False)


class RenameWizard(models.TransientModel):
    _name = 'rename.company.wizard'

    name = fields.Char(string="Rename company", default="Company", required=True)

    def rename_company(self):
        companies = self.env['res.partner'].search([])

        for company in companies:
            if company.company_type == 'company' and not company.is_warehouse:
                if not company.renamed:
                    company.write({'name': company.name + "(" + self.name + ")"})
                    company.renamed = True
                    company.rename_text = "(" + self.name + ")"
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def remove_rename(self):
        companies = self.env['res.partner'].search([])
        for company in companies:
            if company.company_type == 'company':
                text = company.rename_text
                name = company.name
                company.write({'name': name.replace(text, '')})
                company.renamed = False
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
