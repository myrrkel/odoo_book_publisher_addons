# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Specific Vanloo',
    'version': '1.0',
    'author': 'myrrkel',
    'website': 'https://github.com/myrrkel',
    'summary': "Module",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
        'stock',
        'account',
        'sale',
        'crm',
        'purchase',
        'l10n_fr',
    ],
    'category': 'Specific Modules/Vanloo',
    'complexity': 'easy',
    'description': '''
This module adds specific components for Vanloo Book Publisher.
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
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
