from odoo import fields, models


class UoM(models.Model):
    _inherit = "uom.uom"

    code = fields.Char(string="Código")
    symbol = fields.Char(string="Símbolo")
