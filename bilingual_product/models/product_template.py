# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Override the name field to make it translatable
    name = fields.Char(
        'Name',
        index=True,
        required=True,
        translate=True,  # Enable translation
    )

    # Override description_sale to make it translatable
    description_sale = fields.Text(
        'Sales Description',
        translate=True,  # Enable translation
        help="A description of the Product that you want to communicate to your customers. "
             "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note"
    )

    # Virtual fields for Arabic translations (used for CSV import)
    name_ar = fields.Char(
        'Name (Arabic)',
        compute='_compute_name_ar',
        inverse='_inverse_name_ar',
        store=False,
        help="Arabic translation of product name"
    )

    description_sale_ar = fields.Text(
        'Sales Description (Arabic)',
        compute='_compute_description_sale_ar',
        inverse='_inverse_description_sale_ar',
        store=False,
        help="Arabic translation of sales description"
    )

    def _get_arabic_lang_code(self):
        """Get the installed Arabic language code"""
        Lang = self.env['res.lang']
        # Try common Arabic language codes, starting with 'ar'
        for code in ['ar', 'ar_001', 'ar_SY', 'ar_SA', 'ar_EG']:
            if Lang.search([('code', '=', code), ('active', '=', True)], limit=1):
                return code
        return None

    @api.depends('name')
    def _compute_name_ar(self):
        """Get Arabic translation of name"""
        lang_code = self._get_arabic_lang_code()
        for record in self:
            if lang_code:
                record.name_ar = record.with_context(lang=lang_code).name
            else:
                record.name_ar = False

    def _inverse_name_ar(self):
        """Set Arabic translation of name"""
        lang_code = self._get_arabic_lang_code()
        if not lang_code:
            return  # Skip if Arabic not installed
        for record in self:
            if record.name_ar:
                record.with_context(lang=lang_code).name = record.name_ar

    @api.depends('description_sale')
    def _compute_description_sale_ar(self):
        """Get Arabic translation of description"""
        lang_code = self._get_arabic_lang_code()
        for record in self:
            if lang_code:
                record.description_sale_ar = record.with_context(lang=lang_code).description_sale
            else:
                record.description_sale_ar = False

    def _inverse_description_sale_ar(self):
        """Set Arabic translation of description"""
        lang_code = self._get_arabic_lang_code()
        if not lang_code:
            return  # Skip if Arabic not installed
        for record in self:
            if record.description_sale_ar:
                record.with_context(lang=lang_code).description_sale = record.description_sale_ar

    # Note: Fields that remain non-translatable by default:
    # - default_code (Internal Reference)
    # - barcode
    # - list_price (Sales Price)
    # - standard_price (Cost)
    # - weight
    # - type (Product Type)
