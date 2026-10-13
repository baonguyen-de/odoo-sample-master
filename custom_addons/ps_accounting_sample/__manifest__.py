# -*- coding: utf-8 -*-

{
    'name': 'PS Accounting Sample',
    'description': 'PatSoft Accounting Sample module',
    'category': 'PatSoft/Accounting Sample',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/category_views.xml',
        'views/sample_single.xml',
        'views/sample_multiple.xml',
        'views/menus.xml'
    ],
    'demo':[
        'demo/category.csv',
        'demo/sample_multiple.xml',
        'demo/sample_multiple_line.xml',
        'demo/sample_single.xml',
    ],
    'application': True,
}
