# -*- coding: utf-8 -*-
from odoo import models, fields, api


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

    # Note: Fields that remain non-translatable by default:
    # - default_code (Internal Reference)
    # - barcode
    # - list_price (Sales Price)
    # - standard_price (Cost)
    # - weight
    # - type (Product Type)
