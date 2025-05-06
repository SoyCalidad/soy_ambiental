{
    'name': 'Organizador de Soy Ambiental',
    'version': '1.0',
    'description': 'Organiza los menus de Soy Ambiental',
    'summary': 'Organiza los menus de soy Ambiental',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soyambiental',
    'depends': [
        'soyambiental_risk',
        'soyseguridad_contigency_plan',
        'soyseguridad_organization',
        'project',
        'plan_sanitation',
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/menus_data.xml',

        'wizard/ideaa_matrix_wizard_views.xml',
        'wizard/contigency_plan_wizard_views.xml',
        'wizard/programa_ambiental_wizard_views.xml',
        'wizard/plan_ambiental_wizard_views.xml',

        'views/menus.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': False,
}
