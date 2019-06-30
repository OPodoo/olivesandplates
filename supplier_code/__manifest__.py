# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Supplier Code',
    'version': '1.0',
    'category': 'Contacts',
    'summary': 'Supplier Code',
    'license': "AGPL-3",
    'description': """
Supplier Code'
==============================================================

""",
    'author': 'Usman Farzand',
    'support': 'usman_farzand@outlook.com',
    'depends': ['base','contacts','sale','purchase'],
    'images': ['static/description/banner.png'],
    'data': [
        #'security/ir.model.access.csv',
        'views/supplier_code_view.xml',
    ],
    'installable': True,
    
}
