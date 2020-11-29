# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    main_category_id = fields.Many2one('res.partner.category', compute="_compute_main_category", store=True)

    @api.depends('category_id')
    def _compute_main_category(self):
        for rec in self:
            for categ in rec.category_id:
                if categ.is_main:
                    rec.main_category_id = categ
                    break

