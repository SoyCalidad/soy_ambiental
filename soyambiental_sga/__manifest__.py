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
        'data/menus_data.xml',
        'views/menus.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': False,
}
