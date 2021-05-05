# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = ['res.partner']

    is_published = fields.Boolean(default=False)

    website_published = fields.Boolean('Visible on current website', related='is_published', readonly=False)
    # is_published = fields.Boolean('Is Published', copy=False, default=lambda self: self._default_is_published())
    can_publish = fields.Boolean('Can Publish', compute='_compute_can_publish')
    website_url = fields.Char('Website URL', compute='_compute_website_url', help='The full URL to access the document through the website.')

    # @api.depends_context('lang')
    # def _compute_website_url(self):
    #     for record in self:
    #         record.website_url = '#'

    def website_publish_button(self):
        self.ensure_one()
        return self.write({'website_published': not self.website_published})

    def open_website_url(self):
        if self.is_author:
            return {
                'type': 'ir.actions.act_url',
                'url': 'shop/authors?author=%s' % self.id,
                'target': 'self',
            }
        else:
            return super(ResPartner, self).open_website_url()

    @api.model_create_multi
    def create(self, vals_list):
        records = super(ResPartner, self).create(vals_list)
        is_publish_modified = any(
            [set(v.keys()) & {'is_published', 'website_published'} for v in vals_list]
        )
        if is_publish_modified and not all(record.can_publish for record in records):
            raise AccessError(self._get_can_publish_error_message())

        return records

    def write(self, values):
        if 'is_published' in values and not all(record.can_publish for record in self):
            raise AccessError(self._get_can_publish_error_message())

        return super(ResPartner, self).write(values)

    def create_and_get_website_url(self, **kwargs):
        return self.create(kwargs).website_url

    def _compute_can_publish(self):
        """ This method can be overridden if you need more complex rights management than just 'website_publisher'
        The publish widget will be hidden and the user won't be able to change the 'website_published' value
        if this method sets can_publish False """
        for record in self:
            record.can_publish = True

    @api.model
    def _get_can_publish_error_message(self):
        """ Override this method to customize the error message shown when the user doesn't
        have the rights to publish/unpublish. """
        return _("You do not have the rights to publish/unpublish")

