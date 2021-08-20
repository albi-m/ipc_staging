from odoo import api, fields, models
from num2words import num2words


class PosOrderInherit(models.Model):
    _inherit = 'pos.order'


    text_amount_total = fields.Char(string='Amount in Words', compute='get_text_amount')


    def get_text_amount(self):
        text_amount_total = num2words(self.amount_paid, lang='en')
        self.text_amount_total = 'Rupees '+ text_amount_total.replace("point", "and").title() + ' Paisa only'