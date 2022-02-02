{
    'name': 'Leased Property',
    'version': '1.0',
    'summary': 'Leased Property Module',
    'sequence': 16,
    'description':"""
Real Estate
==============
This module was made for internship purpose
    """,
    'category': 'Tools',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['real_estate'],
    'data': [
        'security/ir.model.access.csv',
        'views/leased_property_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}