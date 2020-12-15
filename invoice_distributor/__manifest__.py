# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Invoice Distributor',
    'version': '13.0.0.0',
    'author': 'myrrkel',
    'website': 'https://github.com/myrrkel',
    'summary': "Module",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'stock',
        'sale',
    ],
    'category': 'Generic Modules/Product',
    'complexity': 'easy',
    'description': '''
This module allows to create invoice for distributor. Lines are linked to a final customer.
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
        'views/account_invoice_view.xml',
        'views/res_partner_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
