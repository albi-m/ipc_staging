# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('default_code')
    def _check_default_code(self):
        if self.default_code:
            product_id = self.env['product.template'].search([('default_code', '=', self.default_code)])
            if len(product_id) > 1:
                raise ValidationError("Internal Reference must be unique")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('default_code')
    def _check_default_code(self):
        if self.default_code:
            product_id = self.env['product.product'].search(
                [('default_code', '=', self.default_code)])
            if len(product_id) > 1:
                raise ValidationError("Internal Reference must be unique")
