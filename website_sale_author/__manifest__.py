# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Website Sale Author',
    'version': '13.0.0.0',
    'author': 'myrrkel',
    'website': 'https://github.com/myrrkel',
    'summary': "Add an entry for authors on website",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'contacts',
        'website_sale',
        'website_partner',
        'product_book',
    ],
    'category': 'e-commerce',
    'complexity': 'easy',
    'description': '''
This module adds an entry for authors on website
    ''',
    'qweb': [
    ],
    'demo': [
    ],
    'images': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/website_menu.xml',
        'views/res_partner_author.xml',
        'views/res_partner_author_views.xml',
        'views/website_author_templates.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
