{
    'name': 'Riesgos de Soy Ambiental',
    'description': 'Riesgos de Soy Ambiental',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'version': '1.0',
    'license': 'Other proprietary',
    'category': 'soyambiental',
    'depends': [
        'soyambiental_base',
        'mgmtsystem_process_integration',
        'mgmtsystem_survey',
        'mgmtsystem_opportunity',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/evaluation_views.xml',
        'views/process_evaluation_views.xml',
        'views/ideaa_matrix_views.xml',
        'views/menus.xml',
        'report/ideaa_matrix_xlsx.xml',

        'data/data.xml',
    ],
    'auto_install': False,
    'application': False,
}
