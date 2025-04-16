# -*- coding: utf-8 -*-
{
    'name': 'cl_registro',
    'version': '1.0',
    'summary': 'Gestión',
    'author': 'Liko',
    'category': 'Medical',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/inicio_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cl_registro/static/src/css/clinic_style.css',  
        ],
    },
    'installable': True,
    'application': True,
}