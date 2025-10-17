# -*- coding: utf-8 -*-
from odoo import api, fields, models,_


class Cajero(models.Model):
    _name = "cajero"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Información de los Cajeros"
    _order = 'name'

    name = fields.Char(
        string="Nombre",
        required=True,
        tracking=True,
    )

    activo = fields.Boolean(
        string="Activo",
        default=True,
        tracking=True,
    )

    sucursal = fields.Selection(
        string="Sucursal",
        selection=[
            ('1', 'Central'),
        ],
        required=True,
        tracking=True,
    )

    terminal = fields.Selection(
        string="Caja",
        selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
        ],
        required=True,
        tracking=True,
    )

    empleadoAsignado = fields.Many2one(
        comodel_name="res.users",
        string="Empleado Asignado",
        required=True,
        tracking=True,
    )

    @api.onchange('terminal','sucursal')
    def _onchange_sucursal_terminal(self):
        if self.sucursal != False and self.terminal != False:
            sucursal = ""
            if self.sucursal == "1":
                sucursal = "Central"
            elif self.sucursal == "2":
                sucursal = "Heredia"
            self.name = 'Caja# : ' + self.terminal + ' Sucursal : ' + sucursal


