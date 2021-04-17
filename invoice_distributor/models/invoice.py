# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_distributor = fields.Boolean("Distributor Invoice", related='partner_id.is_distributor')

    def action_post(self):
        res = super(AccountMove, self).action_post()

        for invoice in self.filtered(lambda inv: inv.partner_id.is_distributor):
            _logger.info("Distributor Invoice %s", invoice.name)

            invoice_lines = invoice.mapped('invoice_line_ids').filtered(lambda line: line.partner_id
                                                                        and line.product_id.type == 'product')
            for invoice_line in invoice_lines:
                if invoice_line.sale_line_ids:
                    # Update new quantity
                    for sale_line in invoice_line.sale_line_ids:
                        if invoice_line in sale_line.invoice_lines:

                            for move_line in sale_line.move_ids:
                                move_line.product_uom_qty = invoice_line.quantity
                                move_line.quantity_done = invoice_line.quantity

                            sale_line.product_uom_qty = invoice_line.quantity
                    continue

                # Create sale order and confirmed picking for the account move line
                _logger.info("Invoice Line %s %s", invoice_line.product_id.name, invoice_line.customer_id.name)
                m_sale_order = self.env['sale.order']
                order = m_sale_order.create({'partner_id': invoice_line.customer_id.id,
                                             'partner_invoice_id': invoice_line.partner_id.id,
                                             'warehouse_id': invoice.partner_id.location_id.get_warehouse().id,
                                             'state': 'sale',
                                             })

                order_line = self.env['sale.order.line'].create({'order_id': order.id,
                                                                 'product_id': invoice_line.product_id.id,
                                                                 'product_uom_qty': invoice_line.quantity,
                                                                 'invoice_lines': [(6, 0, [invoice_line.id])]
                                                                 })

                picking = order.picking_ids[0]
                picking.action_confirm()
                picking.move_lines.quantity_done = invoice_line.quantity
                picking.action_done()

        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    customer_id = fields.Many2one('res.partner', string='Customer')

    def unlink(self):
        for line in self:
            if line.move_id.partner_id.is_distributor and line.sale_line_ids:
                raise UserError(_("Invoice line can't be delete if a sale order and a stock move has been created. Cancel it before."))
        res = super(AccountMoveLine, self).unlink()


