from odoo import models, fields, api # type: ignore

class Inicio(models.Model):
    _name = 'cl_registro.inicio'
    _description = 'Pantalla de Inicio'

    name = fields.Char(string="Nombre", default="Inicio", readonly=True)

    def dummy_inventario(self):
        # Método temporal para el botón de Inventario
        return {
            'type': 'ir.actions.act_window',
            'name': 'Inventario',
            'res_model': 'cl_inventario.inicio_inv',
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref('cl_inventario.inicio_inv').id,
        }

    def abrir_expediente(self):
        # Método para redirigir al módulo expediente
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pacientes',
            'res_model': 'medical_partner.res_partner',  # El modelo de pacientes en expediente
            'view_mode': 'kanban,list,form',  # Tipo de vistas que quieres mostrar
            'target': 'current',  # Muestra en la misma ventana
        }
