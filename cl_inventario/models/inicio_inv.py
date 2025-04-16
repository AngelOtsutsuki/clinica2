from odoo import models, fields, api  # type: ignore

class Inicio_Inv(models.Model):
    _name = 'cl_inventario.inicio_inv'
    _description = 'Pantalla de Inicio de Inventario'

    name = fields.Char(string="Nombre", default="Inventario", readonly=True)
    total_medicamentos = fields.Integer(string="Total de Medicamentos", compute="_compute_total_medicamentos")
    total_equipos = fields.Integer(string="Total de Equipos Médicos", compute="_compute_total_equipos")

    def _compute_total_medicamentos(self):
        # Obtener el número de medicamentos registrados
        medicamentos_count = self.env['cl_stock.medicamento'].search_count([])
        self.total_medicamentos = medicamentos_count

    def _compute_total_equipos(self):
        # Obtener el número de equipos médicos registrados
        equipos_count = self.env['cl_equipos.equipo'].search_count([])
        self.total_equipos = equipos_count

    def inventario_equipos(self):
    # Método temporal para el botón de Inventario
        return {
        'type': 'ir.actions.act_window',
        'name': 'Equipos',
        'res_model': 'cl_equipos.equipo',
        'view_mode': 'list,form',
        'target': 'current',
        }

    def inventario_medicamentos(self):
    # Método temporal para el botón de Inventario
        return {
        'type': 'ir.actions.act_window',
        'name': 'Medicamentos',
        'res_model': 'cl_stock.medicamento',
        'view_mode': 'list,form',
        'target': 'current',
        }