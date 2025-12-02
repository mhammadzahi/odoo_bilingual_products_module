# -*- coding: utf-8 -*-
{
    'name': 'Bilingual Products (Arabic/English)',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Enable Arabic and English translations for product fields',
    'description': """
        This module extends the product template to support bilingual content.
        - Makes product Name translatable
        - Makes Sales Description translatable
        - Non-translatable fields: ID, Reference, Barcode, Price, Cost, Weight
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
