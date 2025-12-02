#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import CSV products with bilingual support (Arabic/English)

This script demonstrates how to import products and set translations.
Usage:
    python3 import_bilingual_products.py --csv product_Template.csv --lang ar_001 --arabic-csv product_Template_arabic.csv

For direct Odoo server usage, you can also use this as a reference to create data XML files.
"""

import csv
import argparse
import xmlrpc.client


def import_products_via_xmlrpc(url, db, username, password, csv_file, arabic_csv=None, lang_code='ar_001'):
    """
    Import products via Odoo XML-RPC API with translation support
    """
    # Authenticate
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("Authentication failed!")
        return
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Read English CSV
    products_en = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products_en[row['External ID']] = row
    
    # Read Arabic CSV if provided
    products_ar = {}
    if arabic_csv:
        with open(arabic_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                products_ar[row['External ID']] = row
    
    # Import products
    for ext_id, product_en in products_en.items():
        # Prepare product values
        vals = {
            'name': product_en['Name'],
            'default_code': product_en['Internal Reference'],
            'barcode': product_en['Barcode'] if product_en['Barcode'] else False,
            'list_price': float(product_en['Sales Price']) if product_en['Sales Price'] else 0.0,
            'standard_price': float(product_en['Cost']) if product_en['Cost'] else 0.0,
            'weight': float(product_en['Weight']) if product_en['Weight'] else 0.0,
            'description_sale': product_en['Sales Description'],
            'type': 'product' if product_en['Product Type'] == 'Goods' else 'service',
        }
        
        # Create or update product
        product_id = models.execute_kw(
            db, uid, password,
            'product.template', 'search',
            [[('default_code', '=', vals['default_code'])]]
        )
        
        if product_id:
            # Update existing
            models.execute_kw(
                db, uid, password,
                'product.template', 'write',
                [product_id, vals]
            )
            product_id = product_id[0]
            print(f"Updated product: {vals['name']} (ID: {product_id})")
        else:
            # Create new
            product_id = models.execute_kw(
                db, uid, password,
                'product.template', 'create',
                [vals]
            )
            print(f"Created product: {vals['name']} (ID: {product_id})")
        
        # Add Arabic translation if available
        if ext_id in products_ar:
            product_ar = products_ar[ext_id]
            
            # Update name translation
            if product_ar['Name']:
                models.execute_kw(
                    db, uid, password,
                    'product.template', 'write',
                    [product_id, {'name': product_ar['Name']}],
                    {'context': {'lang': lang_code}}
                )
            
            # Update description translation
            if product_ar['Sales Description']:
                models.execute_kw(
                    db, uid, password,
                    'product.template', 'write',
                    [product_id, {'description_sale': product_ar['Sales Description']}],
                    {'context': {'lang': lang_code}}
                )
            
            print(f"  → Added {lang_code} translation")


def generate_import_xml(csv_file, output_file='product_data.xml'):
    """
    Generate XML data file for direct import into Odoo
    """
    products = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = list(reader)
    
    xml_content = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
'''
    
    for product in products:
        ext_id = product['External ID']
        # Extract just the ID part after the last dot for XML id attribute
        xml_id = ext_id.split('.')[-1] if '.' in ext_id else ext_id
        product_type = 'product' if product['Product Type'] == 'Goods' else 'service'
        
        xml_content += f'''
        <record id="{xml_id}" model="product.template">
            <field name="name">{product['Name']}</field>
            <field name="type">{product_type}</field>
            <field name="default_code">{product['Internal Reference']}</field>
            <field name="barcode">{product['Barcode']}</field>
            <field name="list_price">{product['Sales Price'] if product['Sales Price'] else '0.0'}</field>
            <field name="standard_price">{product['Cost'] if product['Cost'] else '0.0'}</field>
            <field name="weight">{product['Weight'] if product['Weight'] else '0.0'}</field>
            <field name="description_sale">{product['Sales Description']}</field>
        </record>
'''
    
    xml_content += '''
    </data>
</odoo>
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Generated XML file: {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import bilingual products to Odoo')
    parser.add_argument('--csv', required=True, help='Path to English CSV file')
    parser.add_argument('--arabic-csv', help='Path to Arabic CSV file')
    parser.add_argument('--url', default='http://localhost:8069', help='Odoo URL')
    parser.add_argument('--db', help='Database name')
    parser.add_argument('--user', help='Username')
    parser.add_argument('--password', help='Password')
    parser.add_argument('--lang', default='ar_001', help='Arabic language code (default: ar_001)')
    parser.add_argument('--generate-xml', action='store_true', help='Generate XML file instead of importing')
    
    args = parser.parse_args()
    
    if args.generate_xml:
        generate_import_xml(args.csv)
    else:
        if not all([args.db, args.user, args.password]):
            print("Error: --db, --user, and --password are required for XML-RPC import")
            exit(1)
        import_products_via_xmlrpc(
            args.url, args.db, args.user, args.password,
            args.csv, args.arabic_csv, args.lang
        )
