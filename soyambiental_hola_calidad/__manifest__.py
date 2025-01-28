{
    'name': "Soy Ambiental Gestion de Calidad",

    'summary': """
        Soy Ambiental Gestion de calidad""",

    'description': """
        Es necesario instalar lib de python:
            - openpyxl
    """,

    'author': "Soy Calidad",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail', 'account', 'soycalidad_css', 'soyambiental_base'],

    'data': [
        'security/ir.model.access.csv',

        'data/sga_hola_calidad_data.xml',
        'data/sga.hola_calidad.clause.csv',
        'data/sga.hola_calidad.requirement.csv',

        'views/diagnostic_views.xml',

    ],
    'installable': True,
    'application': True,
}
