# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models

class ConsolidatedEwaybill(models.TransientModel):
    _name = "consolidated.ewaybill"
    _description = "Consolidated ewaybill"

    transportation_mode = fields.Selection(
        [
            ('1', 'Road'),
            ('2', 'Rail'),
            ('3', 'Air'),
            ('4', 'Ship')
        ],
        default='1',
        string='Transportation Mode',
        help="""
        Mode of transport is a term used to distinguish substantially different ways to perform.
        The different modes of transport are air, road, rail and ship transport.
        """
    )
    transporter_id = fields.Many2one(
        "ewaybill.transporter",
        string='Transporter',
        ondelete='restrict',
        help="Select transporter for E-Way Bill"
    )
    trans_id = fields.Char(
        related='transporter_id.transporter_id',
        string='Transporter ID',
        help="""
        Transporter ID is a unique identification number allotted to transporters not registered under GST.
        Transporter ID consists of 15 digits.
        """
    )
    state_id = fields.Many2one(
        "res.country.state",
        string='State',
        ondelete='restrict',
        help="State of Supply"
    )
    city = fields.Char(
        string="Place",
        help="Place of consignee"
    )
    vehicle_no = fields.Char(
        string='Vehicle No',
        help="Vehicle No of transporter"
    )
    ewaybill_order_ids = fields.Many2many(
        'sale.order',
        'order_ewaybill_set',
        'order_id',
        'attribute_id',
        string='E-Way Bill Orders',
        help="E-way Bill Approved Orders."
    )

    def consolidatedEwaybill(self):
        ctx = dict(self._context or {})
        saleIds = ctx.get('active_ids')
        saleObjs = self.env['sale.order'].search([('id', 'in', saleIds), ('ewaybill_no', '!=', ''), ('generate_ewaybill', '=', True)])
        partial = self.create({
            'ewaybill_order_ids':[(6, 0, saleObjs.ids)]
        })
        return {
            'name': ("Consolidated E-Way Bill"),
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'consolidated.ewaybill',
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
            'domain': '[]',
        }

    def printBill(self):
        jsonAttachment = self.generateJson()
        if not jsonAttachment:
            raise UserError("Consolidated JSON of E-Way Bill is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (jsonAttachment.id),
            'target': 'new',
        }

    def generateJson(self):
        ewaybillOrderNos = self.ewaybill_order_ids.mapped('ewaybill_no')
        tripSheetEwbBills = []
        for ewaybillOrderNo in ewaybillOrderNos:
            tripSheetEwbBills.append({'ewbno': ewaybillOrderNo})
        transObj = self.transporter_id
        transporterDate = transObj.transporter_date.strftime('%d-%m-%Y')
        consolidateJson = {
            "userGstin": self.trans_id or '',
            "vehicleNo": self.vehicle_no or '',
            "transDocNo": transObj.transporter_doc_no or '',
            "transDocDate": transporterDate or '',
            "fromPlace": self.city or '',
            "transMode": self.transportation_mode or '',
            "fromState": self.state_id.l10n_in_tin or '',
            "tripSheetEwbBills": tripSheetEwbBills or ''
        }
        jsonData = {'tripSheets': [consolidateJson]}
        jsonAttachment = self.env['sale.order'].generatejsonAttachment(jsonData, "consolidatedEwaybillgst.json")
        return jsonAttachment
