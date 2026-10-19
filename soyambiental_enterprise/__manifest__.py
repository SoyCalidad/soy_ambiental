{
    'name': 'Soy Ambiental - Enterprise',
    'description': '''Funcionalidad de Soy Ambiental que depende de módulos Enterprise
    Agrega:
    - Documentos (documents) en el Plan ambiental
    - Documentos (documents) en el Programa ambiental
    ''',
    'summary': 'Dependencias Enterprise de Soy Ambiental',
    'author': 'SoyCalidad',
    'website': 'www.soycalidad.com',
    'version': '18.0.1.0.0',
    'license': 'Other proprietary',
    'category': 'soyambiental',
    'depends': [
        'plan_sanitation',
        'documents',
    ],
    'data': [
        'views/plan_ambiental_views.xml',
        'views/programa_ambiental_views.xml',
    ],
    'auto_install': False,
    'application': False,
}
