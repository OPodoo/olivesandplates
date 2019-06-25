{
    'name': 'Odoo Stock Picking',
    'version': '12.0.1.8',
    'sequence': 4,
    'summary': 'Odoo Stock Picking',
    'price': 20,
    'currency': 'USD',
    'category' : 'Extra Tools',
    'description': """

    Odoo Stock Picking

    """,
    'author': 'Kiran Kantesariya',
    'depends': ['stock'],
    'data': [
             # "views/account_invoice.xml",
             # "views/purchase_invoice.xml",
             # "views/sale.xml",
             # "views/stock_view.xml",
             # "views/product_view.xml",
             # "views/partner.xml",
             "views/picking_view.xml",
             # "views/customer_payment.xml",
             # "views/import_order_lines_view.xml",
             # "views/import_po_lines_view.xml",
             # "views/import_invoice_lines_view.xml",
             # "views/bank_statement.xml",
             # "views/account_move.xml",
             # "views/supp_info.xml",
             # "views/mrp.xml",
             # "views/pricelist.xml"         
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
