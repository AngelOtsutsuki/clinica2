
from odoo.exceptions import ValidationError # type: ignore
from odoo import models, fields, api # type: ignore

class Medicamento(models.Model):
    _name = 'cl_stock.medicamento'
    _description = 'Medicamento'

    nombre_gen = fields.Char(string="Nombre Genérico", required=True)
    nombre_com = fields.Char(string="Nombre Comercial", required=True)
    presentacion = fields.Char(string="Presentación")
    cantidad = fields.Integer(string="Cantidad en inventario", default=0)
    fecha_caducidad = fields.Date(string="Fecha de Caducidad")
    sin_caducidad = fields.Boolean(string="Sin Caducidad", default=False)
    movimiento_ids = fields.One2many(
        'cl_stock.movimiento', 'medicamento_id', string="Movimientos"
    )

    @api.onchange('sin_caducidad')
    def _onchange_sin_caducidad(self):
        if self.sin_caducidad:
            self.fecha_caducidad = False

    @api.constrains('sin_caducidad', 'fecha_caducidad')
    def _check_fecha_caducidad(self):
        for record in self:
            if record.sin_caducidad and record.fecha_caducidad:
                raise ValidationError("No se puede ingresar una fecha de caducidad si el medicamento está marcado como 'Sin Caducidad'.")
            
    def ajustar_cantidad(self, cantidad, tipo):
        """ Ajusta la cantidad de inventario y crea un movimiento. """
        if tipo not in ['entrada', 'salida']:
            raise ValidationError("El tipo de movimiento debe ser 'entrada' o 'salida'.")

        if tipo == 'salida' and self.cantidad < cantidad:
            raise ValidationError("No hay suficiente inventario para realizar la salida.")

        nueva_cantidad = self.cantidad + cantidad if tipo == 'entrada' else self.cantidad - cantidad
        self.cantidad = nueva_cantidad

        self.env['cl_stock.movimiento'].create({
            'medicamento_id': self.id,
            'tipo': tipo,
            'cantidad': cantidad,
            'cantidad_final': nueva_cantidad,
        })
