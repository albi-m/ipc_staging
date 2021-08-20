# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomResPartner(models.Model):
    """ Add gst Number """
    _inherit = 'res.partner'
    _description = 'Add gst Number'

    partner_gst_number = fields.Char('GSTIN Number')
