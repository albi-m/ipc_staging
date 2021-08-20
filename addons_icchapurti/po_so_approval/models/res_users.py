from odoo import api, fields, models




class ResUsersInherit(models.Model):
    _inherit = 'res.users'


    po_approval = fields.Boolean("PO Confirm")
    so_approval = fields.Boolean("SO Confirm")