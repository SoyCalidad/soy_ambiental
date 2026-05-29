# -*- coding: utf-8 -*-
{
    'name': "Revisión por la dirección",
    'description': "Agrega funcionalidad al modulo de Revisión por la dirección, relacionado con la ISO ambiental ",

    'summary': """Agrega funcionalidad al modulo de Revisión por la dirección, relacionado con la ISO ambiental""",

    'author': "Soy Calidad",
    'website': "http://www.soycalidad.com",

    'category': 'Management System',
    'version': '18.0.1.1.0',

    'depends': [
        'base',
        'mgmtsystem_management_review',    
    ],

    'data': [
        'views/management_review_views.xml',
        
        'report/management_review_report.xml',
    ],
}
