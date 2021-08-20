from odoo import api, fields, models,_

class AccountMoveLine(models.Model):
    _inherit = 'res.partner'


    customer_code = fields.Char(string="Partner ID")