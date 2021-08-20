# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import base64
import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError

listedReasons = [
    ('1', 'Transhipment'),
    ('2', 'Vehicle Break down'),
    ('3', 'Not updated earlier')
]


class SaleOrder(models.Model):
    _inherit = "sale.order"

    generate_ewaybill = fields.Boolean(
        string='Generate E-Way Bill',
        help="Enable to generate E-Way Bill"
    )
    transportation_distance = fields.Float(
        string='Distance (Km)',
        help="Distance of transportation"
    )
    mainHsnCode = fields.Integer(
        string='Main HSN Code',
        help="HSN Code of the Product"
    )
    vehicle_no = fields.Char(
        string='Vehicle No',
        tracking=True,
        help="Vehicle No of transporter"
    )
    supply_type = fields.Selection(
        [
            ('I', 'Inward'),
            ('O', 'Outward')
        ],
        string='Supply Type',
        help="Supply whether it is outward/inward."
    )
    sub_supply_type = fields.Selection(
        [
            ('1', 'Supply'),
            ('2', 'Import'),
            ('3', 'Export'),
            ('4', 'Job Work'),
            ('5', 'For Own Use'),
            ('6', 'Job work Returns'),
            ('7', 'Sales Return'),
            ('8', 'Others'),
            ('9', 'SKD/CKD'),
            ('10', 'Line Sales'),
            ('11', 'Recipient Not Known'),
            ('12', 'Exhibition or Fairs'),
        ],
        copy=False,
        string='Sub Supply Type',
        help="Sub types of Supply like supply, export, Job Work etc."
    )
    transportation_mode = fields.Selection(
        [
            ('1', 'Road'),
            ('2', 'Rail'),
            ('3', 'Air'),
            ('4', 'Ship')
        ],
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
    eway_source = fields.Many2one(
        related='warehouse_id.partner_id.state_id',
        string='Source',
        help="Place of consignor"
    )
    eway_destination = fields.Many2one(
        related='partner_id.state_id',
        string='Destination',
        store=True,
        help="Place of consignee"
    )
    ewaybill_no = fields.Char(
        string="E-Way Bill No",
        help="E-Way Bill Attachment"
    )
    reason = fields.Selection(
        listedReasons,
        string='Reason',
        help="Reasons to update vehicle-no"
    )
    remarks = fields.Text(
        string='Remarks',
        help="Remarks to update vehicle-no"
    )
    vehicle_type = fields.Selection(
        [
            ('R', 'Regular'),
            ('O', 'ODC')
        ],
        string='Vehicle Type',
        help="Vehicle whether it is Regular/ODC."
    )

    @api.onchange('transporter_id')
    def onchangeTransporterId(self):
        if self.transporter_id:
            self.transportation_mode = self.transporter_id.transportation_mode

    def generateEWayBill(self):
        jsonAttachment = self.generateJson()
        if not jsonAttachment:
            raise UserError("JSON of E-Way Bill is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (jsonAttachment.id),
            'target': 'new',
        }

    def generateJson(self):
        saleIds = self._context.get('active_ids')
        saleObjs = self.search([('id', 'in', saleIds), ('generate_ewaybill', '=', True)])
        saleJsonList = []
        notewaylist = list(set(saleIds) - set(saleObjs.ids))
        gstEwayVersion = self.env['ir.config_parameter'].sudo().get_param(
            'gst_ewaybill.gst_eway_version') or '1.0.0219'
        for saleObj in saleObjs:
            partnerObj = saleObj.partner_id
            partnerShippingObj = saleObj.partner_shipping_id
            currency = saleObj.currency_id
            amountTotal = saleObj.amount_total
            vehicleType = saleObj.vehicle_type
            if currency.name != 'INR':
                amountTotal = amountTotal * currency.rate
            transporterObj = saleObj.transporter_id
            orderLineData = saleObj.getSaleOrderLineJson()
            sgstValue = orderLineData[0]
            igstValue = orderLineData[1]
            itemdata = orderLineData[2]
            orderJsonDate = saleObj.date_order.strftime('%d/%m/%Y')
            transporterDate = transporterObj.transporter_date.strftime('%d/%m/%Y')
            companyObj = saleObj.warehouse_id.partner_id
            saleJsonData = {
                'genMode': 'Excel',
                'userGstin': companyObj.vat or '',
                'supplyType': saleObj.supply_type or 'I',
                'subSupplyType': int(saleObj.sub_supply_type or 1),
                'docType': 'INV',
                'docNo': saleObj.name or '',
                'docDate': orderJsonDate,
                'fromGstin': companyObj.vat or '',
                'fromTrdName': companyObj.name or '',
                'fromAddr1': companyObj.street or '',
                'fromAddr2': companyObj.street2 or '',
                'fromPlace': companyObj.city or '',
                'fromPincode': int(companyObj.zip or 0),
                'fromStateCode': int(companyObj.state_id.l10n_in_tin or 0),
                'actualFromStateCode': int(companyObj.state_id.l10n_in_tin or 0),
                'toGstin': partnerObj.vat or '',
                'toTrdName': partnerObj.name or '',
                'toAddr1': partnerObj.street or '',
                'toAddr2': partnerObj.street2 or '',
                'toPlace': partnerObj.city or '',
                'toPincode': int(partnerObj.zip or 0),
                'toStateCode': int(partnerObj.state_id.l10n_in_tin or 0),
                'actualToStateCode': int(partnerShippingObj.state_id.l10n_in_tin or 0),
                'totalValue': amountTotal,
                'cgstValue': sgstValue,
                'sgstValue': sgstValue,
                'igstValue': igstValue,
                'totInvValue': amountTotal,
                'mainHsnCode': saleObj.mainHsnCode or 0,
                'cessValue': 0.0,
                'transMode': int(saleObj.transportation_mode),
                'transDistance': saleObj.transportation_distance or '',
                'transporterName': transporterObj.name or '',
                'transporterId': transporterObj.transporter_id or '',
                'transDocNo': transporterObj.transporter_doc_no or '',
                'transDocDate': transporterDate,
                'vehicleNo': saleObj.vehicle_no or '',
                'itemList': itemdata,
                'vehicleType': vehicleType,
            }
            saleJsonList.append(saleJsonData)
        jsonData = {
            'version': gstEwayVersion,
            'billLists': saleJsonList
        }
        jsonAttachment = self.generatejsonAttachment(jsonData, "ewaybillgst.json")
        return jsonAttachment

    def generatejsonAttachment(self, jsonData, jsonFileName):
        jsonAttachment = False
        if jsonData:
            jsonData = json.dumps(jsonData, indent=4, sort_keys=False)
            base64Data = base64.b64encode(jsonData.encode('utf-8'))
            try:
                ewaydata = {
                    'datas': base64Data,
                    'type': 'binary',
                    'res_model': 'sale.order',
                    'db_datas': jsonFileName,
                    'store_fname': jsonFileName,
                    'name': jsonFileName
                }
                jsonObjs = self.env['ir.attachment'].search([('name', '=', jsonFileName)])
                if jsonObjs:
                    jsonAttachment = jsonObjs[0]
                    jsonAttachment.write(ewaydata)
                else:
                    jsonAttachment = self.env['ir.attachment'].create(ewaydata)
            except ValueError:
                pass
        return jsonAttachment

    def getSaleOrderLineJson(self):
        itemList = []
        itemNo = 1
        sgstRateAmount, igstRateAmount = 0.0, 0.0
        for lineObj in self.order_line:
            productObj = lineObj.product_id
            productName = productObj.name
            taxedAmount = lineObj.price_tax
            uqc = 'OTH'
            if lineObj.product_uom:
                uom = lineObj.product_uom.id
                uqcObj = self.env['ewaybill.uqc'].search([('uom', '=', uom)])
                if uqcObj:
                    uqc = uqcObj[0].code
            hsnvalue = productObj.l10n_in_hsn_code or '0'
            hsnCode = hsnvalue.replace('.', '')
            hsnCode = int(hsnCode)
            itemDict = {
                'itemNo': itemNo,
                'productName': productName,
                'productDesc': productName,
                'hsnCode': hsnCode,
                'quantity': lineObj.product_uom_qty,
                'qtyUnit': uqc,
                'taxableAmount': lineObj.price_reduce_taxexcl,
                'sgstRate': 0,
                'cgstRate': 0,
                'igstRate': 0,
                'cessRate': 0,
            }
            if lineObj.tax_id:
                for rateObj in lineObj.tax_id:
                    if rateObj.amount_type == "group":
                        for childObj in rateObj.children_tax_ids:
                            itemDict['sgstRate'] = childObj.amount
                            itemDict['cgstRate'] = childObj.amount
                            sgstRateAmount = sgstRateAmount + taxedAmount / 2
                            break
                    else:
                        itemDict['igstRate'] = rateObj.amount
                        igstRateAmount = igstRateAmount + taxedAmount
                    break
            itemList.append(itemDict)
            itemNo = itemNo + 1
        sgstRateAmount = round(sgstRateAmount, 2)
        igstRateAmount = round(igstRateAmount, 2)
        return [sgstRateAmount, igstRateAmount, itemList]

    def updateVehicleNo(self):
        partial = self.env['vehicle.no.updation'].create(
            {'vehicle_no': self.vehicle_no})
        return {
            'name': ("Update Vehicle No."),
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'vehicle.no.updation',
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'context': self._context,
            'domain': '[]',
        }

    def generateVehicleUpdateJson(self):
        jsonAttachment = self.generateVehicleJson()
        if not jsonAttachment:
            return self.env['wk.wizard.message'].genrated_message(
                "<h3 style='color: #d9534f;'>E-Way Bills are not generated for selected orders</h3>"
            )
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (jsonAttachment.id),
            'target': 'new',
        }

    def generateVehicleJson(self):
        saleIds = self._context.get('active_ids')
        saleObjs = self.search([('id', 'in', saleIds),
                                ('generate_ewaybill', '=', True),
                                ('ewaybill_no', '!=', '')])
        jsonAttachment = False
        if not saleObjs:
            return False
        else:
            vehicleUpdateList = []
            for saleObj in saleObjs:
                transporterObj = saleObj.transporter_id
                companyObj = saleObj.company_id
                transporterDate = transporterObj.transporter_date.strftime(
                    '%d-%m-%Y')
                vehicleUpdateJson = {
                    "ewbno": saleObj.ewaybill_no,
                    "transMode": saleObj.transportation_mode,
                    "vehicleNo": saleObj.vehicle_no or '',
                    "docNo": transporterObj.transporter_doc_no,
                    "docDate": transporterDate,
                    'fromPlace': companyObj.city or '',
                    'fromState': companyObj.state_id.l10n_in_tin or '',
                    "reason": saleObj.reason,
                    "remark": saleObj.remarks or ''
                }
                vehicleUpdateList.append(vehicleUpdateJson)
            jsonData = {'vehicleUpdts': vehicleUpdateList}
            jsonAttachment = self.generatejsonAttachment(jsonData, "vehicleUpdate.json")
        return jsonAttachment
