# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_book = fields.Boolean('Is a Book')
    isbn = fields.Char(string='ISBN')
    release_date = fields.Date(string='Release Date')
    author_id = fields.Many2one('res.partner', 'Author', domain=[('is_author', '=', True)])
    author_ids = fields.Many2many('res.partner', string='Authors', domain=[('is_author', '=', True)])
    authors_name = fields.Char('Authors', compute="_compute_authors_name")

    @api.depends('author_ids', 'author_ids.name')
    def _compute_authors_name(self):
        for product in self:
            product.authors_name = ', '.join(product.author_ids.mapped('name'))

    @api.onchange('is_book')
    def set_default_categ_id(self):
        for rec in self:
            if rec.is_book:
                rec.categ_id = self.env.ref('product_book.product_category_book')