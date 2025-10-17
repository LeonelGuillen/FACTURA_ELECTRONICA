# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    tipo_Identificacion = fields.Selection(
        string="Tipo de Identificación",
        selection=[
            ('1', 'Cédula física'),
            ('2', 'Cédula jurídica'),
            ('3', 'Dimex'),
            ('4', 'Nite'),
            ('10', 'Extranjera'),
        ],
        required=True,
        tracking=True,
    )
    email_copy = fields.Char(string="Correo Copia", help="Email adicional para enviar copia de la factura electrónica.")
    economic_activity_id = fields.Many2one(
        comodel_name="economic.activity", string="Actividad económica por defecto", context={"active_test": False}
    )
    economic_activities_ids = fields.Many2many(
        comodel_name="economic.activity", string="Actividades económicas", context={"active_test": False}
    )

    def action_get_economic_activities(self):
        if self.vat:
            company = self.env["res.company"]
            json_response = company.get_economic_activities(self)
            _logger.debug("E-INV CR  - Economic Activities: %s", json_response)
            if json_response["status"] == 200:
                activities = json_response["activities"]
                # Activity Codes
                a_codes = list([])
                a_ciiu3 = list([])
                for activity in activities:
                    if activity["estado"] == "A":
                        a_codes.append(activity["codigo"])
                        activity_id = self.env["economic.activity"].search([("code", "=", str(activity.get("codigo"))), ("ciiu3", "=", str(activity.get("ciiu3")[0].get("codigo")))], limit=1).id
                        if activity.get("tipo") == "P":
                            self.economic_activity_id = activity_id
                        a_codes.append(activity["codigo"])
                        a_ciiu3.append(activity["ciiu3"][0]["codigo"])
                economic_activities = (self.env["economic.activity"].with_context(active_test=False).search([("code", "in", a_codes), ("ciiu3", "in", a_ciiu3)]))
                economic_activities.active = True
                self.economic_activities_ids = economic_activities
                self.name = json_response["name"]
            else:
                alert = {"title": json_response["status"], "message": json_response["text"]}
                return {"value": {"vat": ""}, "warning": alert}
        else:
            alert = {"title": "Atención", "message": _("Company VAT is invalid")}
            return {"value": {"vat": ""}, "warning": alert}
