{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Real Estate Module',
    'sequence': 15,
    'description':"""
Real Estate
==============
This module was made for internship purpose
    """,
    'category': 'Tools',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['contacts'],
    'data': [
        'security/real_estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_views.xml',
        'views/client_views.xml',
        'views/partner_views.xml',
        
        'wizards/estate_offer_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
}