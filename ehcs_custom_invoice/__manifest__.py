# -*- coding: utf-8 -*-
{
    'name': "EHCS Invoice",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ERP Harbor Consulting Services",
    'website': "http://www.erpharbor.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','account'],
    'data': [
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'qweb': ['static/src/xml/*.xml'], 
}

