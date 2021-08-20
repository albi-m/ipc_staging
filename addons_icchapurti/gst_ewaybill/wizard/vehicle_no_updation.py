# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _

listedReasons = [
    ('1', 'Transhipment'),
    ('2', 'Vehicle Break down'),
    ('3', 'Not updated earlier')
]


class VehicleNoUpdation(models.TransientModel):
    _name = "vehicle.no.updation"
    _description = "Vehicle number updation"

    vehicle_no = fields.Char(
        string='Vehicle No',
        help="Vehicle No of transporter"
    )
    reason = fields.Selection(
        listedReasons,
        default='1',
        string='Reason',
        help="Reasons to update vehicle-no"
    )
    remarks = fields.Text(
        string='Remarks',
        help="Remarks to update vehicle-no"
    )

    def updateVehicleNo(self):
        ctx = dict(self._context or {})
        saleIds = ctx.get('active_ids')
        saleObjs = self.env['sale.order'].search([('id', 'in', saleIds)])
        text = "Unable to update vehicle no"
        if saleObjs:
            vehicle_no = self.vehicle_no
            reason = self.reason
            remarks = self.remarks
            saleObjs.write({
                'vehicle_no': vehicle_no,
                'reason': reason,
                'remarks': remarks,
            })
            reason = dict(listedReasons)[reason]
            text = "Vehicle No: <b>{}</b> for E-Way Bill Order <b>{}</b> has been successfully assigned.".format(vehicle_no, saleObjs.name)
            body = '{}<br/><b>Reason: </b>{} <br/><b>Remarks: </b>{}'.format(text, reason, remarks)
            saleObjs.message_post(body=_(body),subtype='mail.mt_comment')
        return self.env['wk.wizard.message'].genrated_message(text)
