# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_author = fields.Boolean('Is An Author')
    book_ids = fields.Many2many('product.template', string='Books', domain=[('is_book', '=', True)])
    book_count = fields.Integer(compute='_compute_book_count', string='Book Count')

    def _compute_book_count(self):
        self.book_count = len(self.book_ids)
