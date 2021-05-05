# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import http
from odoo.http import request

import odoo.addons.website_sale.controllers.main as WebCtrl # QueryURL, WebsiteSale


class WebsiteSale(WebCtrl.WebsiteSale):
    def _get_search_domain(
        self, search, category, attrib_values, search_in_description=True
    ):
        domain = super()._get_search_domain(
            search, category, attrib_values, search_in_description=search_in_description
        )
        if "author_id" in request.env.context:
            domain.append(("author_id", "=", request.env.context["author_id"]))
        return domain


    @http.route(
        [
            "/shop",
            "/shop/page/<int:page>",
            '/shop/category/<model("product.public.category"):category>',
            '/shop/category/<model("product.public.category"):category'
            ">/page/<int:page>",  # Continue previous line
        ],
        type="http",
        auth="public",
        website=True,
    )
    def shop(self, page=0, category=None, brand=None, search="", **post):
        if brand:
            context = dict(request.env.context)
            context.setdefault("brand_id", int(brand))
            request.env.context = context
        return super().shop(
            page=page, category=category, brand=brand, search=search, **post
        )


    @http.route(
        [
            "/shop/authors",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def author(self, page=0, category=None, author=None, search="", **post):
        m_partner = request.env["res.partner"]
        domain = [('is_author', '=', True)]
        if author:
            partner_sudo = request.env['res.partner'].sudo().browse(int(author))
            is_website_publisher = request.env['res.users'].has_group('website.group_website_publisher')
            if partner_sudo.exists() and (partner_sudo.website_published or is_website_publisher):
                values = {
                    'main_object': partner_sudo,
                    'partner': partner_sudo,
                    'edit_page': False
                }
                return request.render("website_sale_author.author_page", values)
        return request.not_found()

    # Method to get the authors.
    @http.route(["/page/authors"], type="http", auth="public", website=True)
    def authors(self, **post):
        m_partner = request.env["res.partner"]
        domain = [('is_author', '=', True)]
        if post.get("search"):
            domain += [("name", "ilike", post.get("search"))]
        author_rec = m_partner.sudo().search(domain)

        keep = WebCtrl.QueryURL("/page/authors", author_id=[])
        values = {"author_rec": author_rec, "keep": keep}
        if post.get("search"):
            values.update({"search": post.get("search")})
        return request.render("website_sale_author.res_partner_authors", values)
