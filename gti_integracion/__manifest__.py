{
    'name': 'Integración GTI',
    'version': '1.0',
    'category': 'Facturación Electrónica',
    'summary': 'Manejo de Facturación',
    'sequence': -100,
    'description': "",
    'author': 'Greivin Gamboa Flores',
    'website': 'http://leoguillen.com',
    'license': 'LGPL-3',
    'depends': [
        'mail',
        'account',
        'sale',
        'hr',
    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Data
        'data/discount_code_data.xml',
        'data/economic_activity_data.xml',
        'data/uom_data.xml',
        'data/res_currency_data.xml',
        # Wizards
        # 'wizard/sa_estudiante_pre_matricula_wizard_view.xml',
        # Views
        'views/view_cajero_menu.xml',
        'views/uom_views.xml',
        'views/res_currency_views.xml',
        'views/view_product_template_inherit.xml',
        'views/view_product_product_inherit.xml',
        'views/view_res_company_inherit.xml',
        'views/view_account_move_inherit.xml',
        'views/view_config_settings.xml',
        'views/view_res_partner_inherit.xml',
        'views/view_account_tax_inherit.xml',
        'views/view_cajero.xml',
        'views/view_documento_hacienda.xml',

        # reports
        # 'report/report_accion_personal_vacaciones.xml'

    ],
    'assets': {
        'web.assets_backend': [
            # 'sa_periodo/static/src/js/sa_periodo_dashboard.js',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
