# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Partner Bookshop Import',
    'version': '13.1.0.0',
    'author': 'myrrkel',
    'website': 'https://github.com/myrrkel',
    'summary': "Module",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
        'base_geolocalize',
        'phone_validation',
    ],
    'category': 'Generic Modules/Partner',
    'complexity': 'easy',
    'description': '''
This module allows to create partners from bookshop lists on internet.
    ''',
    'qweb': [
    ],
    'demo': [
    ],
    'images': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/partner_bookshop_import_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
