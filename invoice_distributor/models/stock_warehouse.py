# -*- coding: utf-8 -*-
# Copyright (C) 2021 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    is_distributor = fields.Boolean("Is Distributor", related='partner_id.is_distributor')
