{
    'name': 'Gestión de Medicamentos',
    'version': '1.0',
    'author': 'Tu Nombre',
    'category': 'Healthcare',
    'summary': 'Gestión de medicamentos en una clínica',
    'description': """
    Módulo para la gestión de medicamentos, permitiendo agregar, actualizar y consultar inventarios.
    """,
    'depends': ['base'],  # Agrega dependencias necesarias
    'data': [
        'security/ir.model.access.csv',  # Archivo de permisos
        'views/medicamento.xml',  # Vistas de medicamentos
        'views/menu.xml',  # Menú principal (si es necesario)
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

