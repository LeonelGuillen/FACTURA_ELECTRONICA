# -*- coding:utf-8 -*-

from odoo.addons.base.models.res_partner import _tz_get
from odoo import api, fields, models, _
import requests
import logging
import traceback

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    gti_NumCuenta = fields.Integer(string="Número de Cuenta", required=False)
    gti_Usuario = fields.Char(string="Usuario" ,required=False)
    gti_Clave = fields.Char(string="Clave", required=False)
    gti_Url = fields.Char(string="URL API",required=False)
    codigo_actividad = fields.Char(string="Codigo de Actividad", required=True, tracking=True)

    tz = fields.Selection(_tz_get, string="Zona horaria")
    economic_activity_id = fields.Many2one(
        comodel_name="economic.activity", string="Actividad económica", context={"active_test": False}
    )
    economic_activities_ids = fields.Many2many(
        comodel_name="economic.activity", string="Actividades económicas", context={"active_test": False}
    )
    environment = fields.Selection(
        selection=[("disabled", "Deshabilitado"), ("api-stag", "Pruebas"), ("api-prod", "Producción")],
        string="Ambiente",
        required=True,
        default="disabled"
    )
    gti_url = fields.Char(string="GTI URL", compute="_compute_gti_url")

    def _compute_gti_url(self):
        for company in self:
            if company.environment == "api-stag":
                company.gti_url = "https://pruebas.gticr.com/AplicacionFEPruebas/ApiCargaFactura/api"
            elif company.environment == "api-prod":
                company.gti_url = "https://www.facturaelectronica.cr/ApiCargaFactura/api"
            else:
                company.gti_url = ""

    def get_economic_activities(self, company):
        # Mensaje del Ministerio de Hacienda:
        # Para garantizar la compatibilidad y la seguridad, solo permitimos el uso de navegadores que estén,
        # como máximo, tres versiones detrás de la versión más reciente lanzada por el fabricante. Esto se debe a que
        # las versiones más antiguas de los navegadores pueden no tener las últimas actualizaciones de seguridad y
        # pueden no ser compatibles con todas las funciones de nuestros sistemas
        url_chrome = "https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/all/versions"
        response_chrome_version = requests.get(url_chrome)
        data = response_chrome_version.json()
        latest_version = data['versions'][0]['version']
        endpoint = "https://api.hacienda.go.cr/fe/ae?identificacion=" + company.vat
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,/;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "api.hacienda.go.cr",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{latest_version} Safari/537.36"
        }
        try:
            response = requests.get(endpoint, headers=headers, verify=False)
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            _logger.error("get_economic_activities: Exception connecting to Hacienda API: %s\n%s", str(e), tb)
            return {"status": -1, "text": "Excepcion %s" % e}

        if 200 <= response.status_code <= 299:
            _logger.debug("FECR - get_economic_activities response: %s", (response.json()))
            response_json = {
                "status": 200,
                "activities": response.json().get("actividades"),
                "name": response.json().get("nombre"),
            }
        # elif 400 <= response.status_code <= 499:
        #    response_json = {'status': 400, 'ind-estado': 'error'}
        else:
            _logger.error("FECR - get_economic_activities failed.  error: %s", response.status_code)
            response_json = {
                "status": response.status_code,
                "text": "get_economic_activities failed: %s" % response.reason,
            }
        return response_json

    def action_get_economic_activities(self):
        if self.vat:
            json_response = self.get_economic_activities(self)
            _logger.debug("E-INV CR  - Economic Activities: %s", json_response)
            if json_response["status"] == 200:
                activities = json_response["activities"]
                a_codes = list([])
                a_ciiu3 = list([])
                for act in activities:
                    if act.get("estado") == "A":
                        activity_id = self.env["economic.activity"].search([("code", "=", str(act.get("codigo"))), ("ciiu3", "=", str(act.get("ciiu3")[0].get("codigo")))], limit=1).id
                        if act.get("tipo") == "P":
                            self.economic_activity_id = activity_id
                        a_codes.append(act["codigo"])
                        a_ciiu3.append(act["ciiu3"][0]["codigo"])
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
