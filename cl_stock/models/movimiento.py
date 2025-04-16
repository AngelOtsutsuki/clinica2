from odoo.exceptions import ValidationError # type: ignore
from odoo import models, fields, api # type: ignore

class Movimiento(models.Model):
    _name = 'cl_stock.movimiento'
    _description = 'Movimiento de Inventario'

    medicamento_id = fields.Many2one('cl_stock.medicamento', string="Medicamento", required=True)
    tipo = fields.Selection([('entrada', 'Entrada'), ('salida', 'Salida')], string="Tipo de Movimiento", required=True)
    cantidad = fields.Integer(string="Cantidad", required=True)
    cantidad_final = fields.Integer(string="Cantidad Final", readonly=True)
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        # Obtenemos el medicamento
        medicamento = self.env['cl_stock.medicamento'].browse(vals['medicamento_id'])

        # Validamos que haya suficiente inventario para movimientos de tipo salida
        if vals['tipo'] == 'salida' and medicamento.cantidad < vals['cantidad']:
            raise ValidationError("No hay suficiente inventario para realizar la salida.")

        # Ajustamos la cantidad de inventario
        nueva_cantidad = medicamento.cantidad + vals['cantidad'] if vals['tipo'] == 'entrada' else medicamento.cantidad - vals['cantidad']
        medicamento.cantidad = nueva_cantidad

        # Guardamos la cantidad final en el movimiento
        vals['cantidad_final'] = nueva_cantidad

        # Creamos el movimiento
        movimiento = super(Movimiento, self).create(vals)
        return movimiento

    def unlink(self):
        for movimiento in self:
            # Restauramos la cantidad al eliminar un movimiento
            if movimiento.tipo == 'entrada':
                movimiento.medicamento_id.cantidad -= movimiento.cantidad
            elif movimiento.tipo == 'salida':
                movimiento.medicamento_id.cantidad += movimiento.cantidad

        return super(Movimiento, self).unlink()
