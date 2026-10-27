{
    'name': 'Riesgos de Soy Ambiental',
    'description': '''Riesgos de Soy Ambiental
    Agrega:
    - Matriz IDEAA
    ''',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'version': '18.0.1.0.0',
    'license': 'Other proprietary',
    'category': 'soyambiental',
    'depends': [
        'soyambiental_base',
        'mgmtsystem_process_integration',
        'mgmtsystem_survey',
        'mgmtsystem_opportunity',
        'mgmtsystem_action',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ideaa_matrix_views.xml',
        'views/menus.xml',
        'report/ideaa_matrix_xlsx.xml',
    ],
    'auto_install': False,
    'application': False,
}
