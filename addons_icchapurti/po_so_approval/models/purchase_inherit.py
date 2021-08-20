from odoo import api, fields, models



class SaleOrderInherit(models.Model):
    _inherit = 'purchase.order'


    po_confirm = fields.Boolean("PO Confirm", compute='get_user_access')



    def get_user_access(self):
        if self.env.user.id == 2:
            self.po_confirm = True
        else:
            self.po_confirm = self.env.user.po_approval

    def action_button_confirm(self):
        self.button_confirm()