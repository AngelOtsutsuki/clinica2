from odoo import models, fields, api, exceptions # type: ignore

class Equipo(models.Model): 
    _name = 'cl_equipos.equipo'
    _description = 'Equipo'

    nombre = fields.Char(string="Nombre", required=True)
    estado = fields.Selection([('activo', 'Activo'), ('inactivo', 'Inactivo')], string="Estado", required=True, default='activo')
    numero_inv = fields.Char(string="Número de Inventario", default=0)
    ubicacion = fields.Char(string="Ubicación")
    fecha_ultimo_mantenimiento = fields.Date(string="Último Mantenimiento")
    active = fields.Boolean(string="Activo", default=True)

    @api.onchange('estado')
    def _onchange_estado(self):
        """Cambia automáticamente el campo 'active' según el estado del equipo."""
        for record in self:
            record.active = record.estado == 'activo'

    @api.model
    def create(self, vals):
        """Asegura que el campo active se sincronice con el estado en la creación."""
        if 'estado' in vals and vals['estado'] == 'inactivo':
            vals['active'] = False
        return super(Equipo, self).create(vals)

    def write(self, vals):
        """Sincroniza el campo 'active' con el estado al actualizar."""
        if 'estado' in vals:
            vals['active'] = vals['estado'] == 'activo'
        return super(Equipo, self).write(vals)


