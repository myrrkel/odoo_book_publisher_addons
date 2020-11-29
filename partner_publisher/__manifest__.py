# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Partner Publisher',
    'version': '13.0.0.0',
    'author': 'myrrkel',
    'website': 'https://github.com/myrrkel',
    'summary': "Module",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product_book',
    ],
    'category': 'Generic Modules/Product',
    'complexity': 'easy',
    'description': '''
This module adds specific partner views for book publisher.
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
        'views/res_partner_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
