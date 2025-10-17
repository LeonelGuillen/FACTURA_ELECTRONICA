from odoo import fields, models


class DiscountCode(models.Model):
    _name = "discount.code"
    _description = "Código de Descuento"
    _order = "sequence, id"

    active = fields.Boolean(string="Activo", default=True)
    code = fields.Char(string="Código", required=True)
    sequence = fields.Char(string="Secuencia")
    name = fields.Char(string="Nombre", required=True)
