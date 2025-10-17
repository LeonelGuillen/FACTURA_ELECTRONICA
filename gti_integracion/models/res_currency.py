from odoo import fields, models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    code = fields.Char(string='Código', help='Código utilizado en facturación electrónica')
