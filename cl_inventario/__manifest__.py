# -*- coding: utf-8 -*-
{
    'name': 'cl_inventario',
    'version': '1.0',
    'summary': 'Inventario',
    'author': 'angel',
    'category': 'Medical',
    'depends': ['base'],
    'data': [
    'security/ir.model.access.csv',
    'views/inicio_inv.xml',

],
'assets': {
    'web.assets_backend': [
        'cl_registro/static/src/css/clinic_style.css',  
    ],
},
    'installable': True,
    'application': True,
}

