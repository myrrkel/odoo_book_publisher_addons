# -*- coding: utf-8 -*-
# Copyright (C) 2021 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    is_distributor = fields.Boolean("Is Distributor")

    @api.onchange('is_distributor')
    def _onchange_is_distributor(self):
        if not self.is_distributor:
            return
        domain = [('is_distributor', '=', True)]
        distributor_ids = self.env['res.partner'].search(domain)
        warehouse_ids = self.env['stock.warehouse'].search(domain)
        if distributor_ids:
            self.partner_invoice_id = distributor_ids[0]
        if warehouse_ids:
            self.warehouse_id = warehouse_ids[0]
        return {'domain': {'partner_invoice_id': domain, 'warehouse_id': domain}}

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self._onchange_is_distributor()

    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        result['partner_shipping_id'] = self.partner_invoice_id.id
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self):
        result = super(SaleOrderLine, self)._prepare_invoice_line()
        result['customer_id'] = self.order_id.partner_id.id
        return result
