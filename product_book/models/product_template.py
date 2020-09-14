# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_book = fields.Boolean('Is a Book', compute='_compute_is_book')
    isbn = fields.Char(string='ISBN')
    author_id = fields.Many2one('res.partner', 'Author', domain=[('is_author', '=', True)])

    @api.depends('categ_id')
    def _compute_is_book(self):
        for product in self:
            _logger.info("_compute_is_book product_category_book %s", self.env.ref('product_book.product_category_book'))
            if product.categ_id.id == self.env.ref('product_book.product_category_book').id:
                product.is_book = True
            else:
                product.is_book = False
