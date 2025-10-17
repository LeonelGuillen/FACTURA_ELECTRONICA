# -*- coding: utf-8 -*-
from odoo import fields, models, api


class EconomicActivity(models.Model):
    _name = "economic.activity"
    _description = "Actividades económicas"
    _order = "code"

    active = fields.Boolean(string="Activo", default=True)
    code = fields.Char(string="Código")
    name = fields.Char(string="Nombre")
    description = fields.Char(string="Descripción")
    ciiu3 = fields.Char(string="CIIU 3")
    sale_type = fields.Selection(selection=[("goods", "Goods"), ("services", "Services")], default="goods", required=True)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        domain = args + ["|", "|", ("name", operator, name), ("code", operator, name), ("ciiu3", operator, name)]
        activities = self.search_fetch(domain, ['display_name'], limit=limit)
        return [(a.id, a.display_name) for a in activities]

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.code}] {record.name}"
