# -*- coding:utf-8 -*-

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_code_id = fields.Many2one('discount.code', string="Código de Descuento")
