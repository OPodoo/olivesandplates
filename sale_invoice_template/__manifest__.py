# -*- coding: utf-8 -*-
{
	"name" : "Sale Invoice Customised Report ",
	"version" : "12.0.2",
	'sequence': 1,
	"depends" : ['base','sale_management','account'],
	'author': "Kiran Kantesariya",
	"support" : "kiran.backup0412@gmail.com",
	"category" : "Sales Management",
	"description": """ Sale Invoice Report""",
	'summary': 'Sale Invoice Report',
	"data": [
		'views/sale_invoice_view.xml',
	],
	"auto_install": False,
	"installable": True,
}
