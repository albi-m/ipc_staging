# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models

class EwaybillUqc(models.Model):
    _name = "ewaybill.uqc"
    _description = "Ewaybill UQC"

    name = fields.Char(
        string="Unit",
        help="UQC (Unit of Measure) of goods sold"
    )
    code = fields.Char(
        string="Code",
        help="Code for UQC (Unit of Measure)"
    )
    uom = fields.Many2one(
        "uom.uom",
        string="Units of Measure",
        help="Units of Measure use for all stock operation"
    )
