{
    'name': 'Creación del módulo de plan de saneamiento ambiental para Soy Ambiental',
    'version': '18.0.1.0.0',
    'description': 'Creación del módulo de plan de saneamiento ambiental para Soy Ambiental',
    'summary': 'Creación del módulo de plan de saneamiento ambiental Soy Ambiental',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'ambiental',
    'depends': [
        'mgmtsystem_process_integration',
        'dms',
        'soycalidad_improve',
        'account'
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/onboarding_data.xml',
        'views/plan_ambiental.xml',
        'views/programa_ambiental.xml',
        'views/ambient.xml',
        'views/plan_sanidad_templates.xml',
        'views/menu.xml',
        'wizards/plan_ambiental_r.xml',
        'wizards/programa_ambiental_r.xml',
        'reports/plan_ambiental_reports.xml',
        'reports/programa_ambiental_report.xml',
        'data/mail_template_data.xml'
    ],
    'images': ['static/description/icon.jpg'],
    'auto_install': False,
    'application': True,
}
