{
    'name': 'Medical Partner',
    'version': '1.0',
    'category': 'Medical',
    'summary': 'Gestión de citas médicas y pacientes',
    'description': """
        Módulo para la gestión de citas médicas y pacientes
    """,
    'depends': ['base', 'mail'],  
    'data': [
        'security/user_profile_groups.xml',
        'security/medical_security.xml',
        'security/ir.model.access.csv',
        'views/paciente.xml',
        'views/lista_cita.xml',
        'views/formulario_cita.xml',
        'views/inicio.xml',
        'views/menu.xml',
    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
