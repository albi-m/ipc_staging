# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gst_eway_version = fields.Char(
        string="GST E-Way Tool Version",
        help="""
        GST e-Way Bill System Bulk Generation Attributes & Tools Version
        Follow below link to get to latest version
        
        => https://docs.ewaybillgst.gov.in/html/formatdownloadnew.html

        """)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            "gst_ewaybill.gst_eway_version", self.gst_eway_version
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update({
            'gst_eway_version': self.env['ir.config_parameter'].sudo().get_param('gst_ewaybill.gst_eway_version'),
        })
        return res
