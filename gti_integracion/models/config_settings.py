# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gti_NumCuenta = fields.Integer(
        string="Número de Cuenta",
        required=False,
    )

    gti_Usuario = fields.Char(
        string="Usuario",
        required=False,
    )

    gti_Clave = fields.Char(
        string="Clave",
        required=False,
    )

    gti_Url = fields.Char(
        string="URL API",
        required=False,
    )

    def set_values(self):
        """
            Asigna los valores de la configuracion guardada
        :return: valores de la configuracion
        """
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('gti_integracion.gti_NumCuenta', self.gti_NumCuenta)
        self.env['ir.config_parameter'].set_param('gti_integracion.gti_Usuario', self.gti_Usuario)
        self.env['ir.config_parameter'].set_param('gti_integracion.gti_Clave', self.gti_Clave)
        self.env['ir.config_parameter'].set_param('gti_integracion.gti_Url', self.gti_Url)


    @api.model
    def get_values(self):
        """
            obtiene los valores de la configuracion para ser guardados
        :return: valores asignados
        """
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        gti_NumCuenta = ICPSudo.get_param('gti_integracion.gti_NumCuenta')
        gti_Usuario = ICPSudo.get_param('gti_integracion.gti_Usuario')
        gti_integracion_Clave = ICPSudo.get_param('gti_integracion.gti_Clave')
        gti_Url = ICPSudo.get_param('gti_integracion.gti_Url')
        res.update(
            gti_NumCuenta = gti_NumCuenta,
            gti_Usuario = gti_Usuario,
            gti_Clave = gti_integracion_Clave,
            gti_Url = gti_Url,
        )
        return  res
