from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    case_size = fields.Float(string='CASE SIZE')
    size = fields.Char(string='Size')
    mrp = fields.Float(string='MRP')
    jio_price = fields.Float(string='Unit Price/Sales Price')
    bp_per_margin = fields.Float(string='BP % MARGIN')
    hsn_code = fields.Char(string='HSN Code')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_code = fields.Char(string='Product Code', compute='_get_product_code')


    @api.depends('categ_id')
    def _get_product_code(self):
        get_product_cat = self.categ_id.complete_name.upper().split('/')
        a = get_product_cat[0][0:2]
        d = str(self.id).zfill(6)
        if len(get_product_cat) == 1:
            lst1 = get_product_cat
            lst = lst1 + get_product_cat
            b = lst[1].replace(" ","")[0:2]
        else:
            b = get_product_cat[1].replace(" ","")[0:2][0:2]
        brand = self.product_brand_id.name
        if brand:
            c = brand.upper()[0:2]
        else:
            c = b
        self.product_code = a+b+c+d

class Company(models.Model):
    _inherit = "res.company"

    pan_number = fields.Char(string='PAN Number')