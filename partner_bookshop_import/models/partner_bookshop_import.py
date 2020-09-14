# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
import logging
import requests
import base64
from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)


class PartnerBookshopImport(models.Model):
    _name = 'partner.bookshop.import'

    name = fields.Char('Name')
    url = fields.Char('Url')
    import_type = fields.Selection(string='Import Type', selection='_get_import_type_selection')
    partner_category_id = fields.Many2one('res.partner.category', string='Category')

    def _get_import_type_selection(self):
        return [('getshoplist', 'getShopList'),
                ('ajax', 'Ajax'),
                ('json', 'Json'),
                ('HTML', 'HTML')]

    def import_partners(self):

        try:
            r = requests.get(self.url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'})
            html = r.text

        except requests.exceptions.HTTPError as err:
            _logger.error(err)
            return -1

        if self.import_type == 'getshoplist':
            self.import_partners_getshoplist(html)

    def import_partners_getshoplist(self, html):
        soup = BeautifulSoup(html, "html.parser")
        partner_o = self.env['res.partner']

        for contact in soup.find_all("div", {"class": "bloc_detail_lib"}):
            if self.partner_category_id:
                values = {"is_company": True}
                values['category_id'] = [(4, self.partner_category_id.id)]
                values['country_id'] = self.env.ref('base.fr').id

            for bloc_nom_lib in contact.findAll("div", {"class": "bloc_nom_lib"}):
                values['name'] = bloc_nom_lib.getText().strip()

            for adresse_lib in contact.findAll("div", {"class": "adresse_lib"}):
                for code_postal in adresse_lib.findAll("p", {"class": "code_postal"}):
                    values['zip'] = code_postal.getText().strip()
                    code_postal.decompose()
                for city in adresse_lib.findAll("p", {"class": "city"}):
                    values['city'] = city.getText().strip()
                    city.decompose()

                values['street'] = adresse_lib.getText().replace("\n", "").strip()

            for tel_lib in contact.findAll("div", {"class": "tel_lib"}):
                for link in tel_lib.findAll("a"):
                    href = link.attrs.get('href')
                    if href[:4] == "tel:":
                        values['phone'] = partner_o.phone_format(href[4:].replace('-', '').strip())
                    if href[:7] == "mailto:":
                        values['email'] = href[7:].strip()

            partner_exists = self.search_partner(values['phone'], values['email'])

            for itineraire_lib in contact.findAll("div", {"class": "itineraire_lib"}):
                for link in itineraire_lib.findAll("a"):
                    gmap_href = link.attrs.get('href')
                    _logger.info("gmap_href: %s", gmap_href)
                    geo_loc = self.extract_geo_localization(gmap_href)
                    if geo_loc:
                        values['partner_latitude'] = geo_loc[0]
                        values['partner_longitude'] = geo_loc[1]
                        continue

            for horaires_lib in contact.findAll("div", {"class": "libItem-horaires-icone"}):
                for link in horaires_lib.findAll("button"):
                    opening_time = link.attrs.get('data-original-title')
                    _logger.info("opening_time: %s", opening_time)

            _logger.info("values: %s", values)

            if not partner_exists:
                for img in contact.findAll("img", {"class": "LogoMag"}):
                    logo_src = img.attrs.get('data-src')
                    _logger.info("logo_src: %s", logo_src)
                    if logo_src:
                        try:
                            r = requests.get(logo_src, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'})
                            values['image_1920'] = base64.b64encode(r.content)

                        except requests.exceptions.HTTPError as err:
                            _logger.error(err)

                _logger.info("CREATE PARTNER")
                partner = self.env['res.partner'].create(values)
            else:
                # Update values for of previously added partner
                if values.get('partner_latitude', False) and values.get('partner_longitude', False):
                    update_values = {}
                    if values['partner_latitude'] != partner_exists.partner_latitude:
                        update_values['partner_latitude'] = values['partner_latitude']
                    if values['partner_longitude'] != partner_exists.partner_longitude:
                        update_values['partner_longitude'] = values['partner_longitude']
                    if update_values:
                        partner_exists.update(update_values)


    def search_partner(self, phone, email):
        domain = ""
        if phone and email:
            domain = ['|', ('phone', '=', phone), ('email', '=', email)]
        elif phone:
            domain = [('phone', '=', phone)]
        elif email:
            domain = [('email', '=', email)]

        if domain:
            domain.append(('is_company', '=', True))
            return self.env['res.partner'].with_context(active_test=False).search(domain)
        else:
            return False

    def extract_geo_localization(self, path):
        '''
        https://www.google.fr/maps/dir/xxxx/@47.8723312,-3.9217445,13z/?hl=fr
        :param path:
        :return:
        '''
        datas = path.split('/')
        for data in datas:
            if data[:1] == "@":
                geo_datas = data[1:].split(',')
                if len(geo_datas) == 3:
                    return geo_datas[0], geo_datas[1]
        return False
