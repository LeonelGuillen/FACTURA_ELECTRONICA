# -*- coding:utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cabys = fields.Char(
        string="Codigo CABYS",
        required=True,
        tracking=True,
    )
    impuesto = fields.Boolean(
        string="Tiene Impuesto",
        default=True
    )
