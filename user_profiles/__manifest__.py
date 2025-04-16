{
    'name': 'User Profiles',
    'version': '1.0',
    'category': 'Medical',
    'summary': 'Gestión de perfiles de usuario para sistema médico',
    'description': """
        Este módulo permite gestionar perfiles de usuario para un sistema médico,
        permitiendo diferenciar entre pacientes, doctores y personal administrativo.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [ 'medical_partner'],
    'data': [
        'security/ir.model.access.csv',
        'views/user_profile_views.xml',
        'views/templates.xml',
        'views/wizard_create_profile.xml',
        'views/menus.xml',
        'views/patient_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
