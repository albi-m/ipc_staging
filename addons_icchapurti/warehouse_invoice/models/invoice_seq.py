# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InvoiceSequence(models.Model):
    _inherit = 'account.move'

    def _compute_seq(self):
        """
        To Generate Sequence number
        """
        for rec in self:
            # rec.compute_seq = False
            sale_order_id = self.invoice_line_ids.mapped(
                'sale_line_ids').order_id
            if sale_order_id and not rec.custom_invoice_ref:
                warehouse = sale_order_id.warehouse_id
                sequence_id = warehouse.invoice_sequence
                if not sequence_id:
                    vals = {
                        'name': _('Invoice Sequence %s') % warehouse.name,
                        'code': '%s-invoice' % warehouse.code,
                        'implementation': 'no_gap',
                        'prefix': warehouse.code.replace(" ", "") + "/%(year)s/",
                        'suffix': '',
                        'padding': 4,
                        'number_next': 1,
                        'company_id': warehouse.company_id.id}
                    sequence_id = self.env['ir.sequence'].sudo().create(vals)
                    warehouse.write({
                        'invoice_sequence': sequence_id.id
                    })
                sequence_number = self.env['ir.sequence'].next_by_code(
                    sequence_id.code)
                rec.update({
                    'custom_invoice_ref': sequence_number
                })
                return sequence_number

    def action_post(self):
        res = super(InvoiceSequence, self).action_post()
        self._compute_seq()
        self.name = self.custom_invoice_ref
        self.payment_reference = self.custom_invoice_ref
        return res

    custom_invoice_ref = fields.Char(string="Invoice Sequence", store=True)
    compute_seq = fields.Boolean(default=True)


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    invoice_sequence = fields.Many2one('ir.sequence')
