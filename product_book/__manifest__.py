# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Product Book',
    'version': '13.0.0.0',
    'author': 'myrrkel',
    'website': 'https://github.com/myrrkel',
    'summary': "Book product with author",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'contacts',
        'product_template_tags',
    ],
    'category': 'Generic Modules/Product',
    'complexity': 'easy',
    'description': '''
This module adds a book product category.
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
        'data/product_category.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
