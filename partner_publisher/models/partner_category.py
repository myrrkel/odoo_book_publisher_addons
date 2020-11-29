# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class PartnerCategory(models.Model):
    _description = 'Partner Tags'
    _inherit = "res.partner.category"

    is_main = fields.Boolean(string="Is Main")
