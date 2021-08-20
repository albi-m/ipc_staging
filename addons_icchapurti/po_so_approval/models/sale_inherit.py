from odoo import api, fields, models



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'


    so_confirm = fields.Boolean("SO Confirm", compute='get_user_access')


    def get_user_access(self):
        if self.env.user.id == 2:
            self.so_confirm = True
        else:
            self.so_confirm = self.env.user.so_approval


    def action_button_confirm(self):
        self.action_confirm()