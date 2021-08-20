# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        company_ids = self.env['res.company'].search(
            [('resupply_company', '!=', False)])
        seller_ids = []
        for company in company_ids:
            print("Company ", company.name)
            products = self.env['product.template'].search([('seller_ids', '=', False)])
            values = {
                'name': company.resupply_company.partner_id.id,
                'company_id': company.id
            }
            seller = (0, 0, values)
            seller_ids.append(seller)
        print(seller_ids)
        products.sudo().write({
            'seller_ids': seller_ids
        })
        return res
