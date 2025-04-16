# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class CitaMedica(models.Model):
    _name = 'cita.medica'
    _description = 'Cita Médica'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'
    
    name = fields.Char(string='Referencia', required=True, copy=False, 
                      readonly=True, default=lambda self: _('Nueva Cita'))
    partner_id3 = fields.Many2one('res.partner', string='Paciente', required=True, 
                                domain=[('is_patient', '=', True)], tracking=True)
    doctor_id = fields.Many2one('inicio.medico', string='Médico', required=True, tracking=True)
    date = fields.Datetime(string='Fecha y Hora', required=True, tracking=True)
    end_date = fields.Datetime(string='Fin', compute='_compute_end_date', store=True)
    duration = fields.Float(string='Duración', default=0.5, help='Duración en horas')
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada')
    ], string='Estado', default='draft', tracking=True)
    
    notes = fields.Text(string='Notas')
    reason = fields.Text(string='Motivo de la consulta')
    diagnosis = fields.Text(string='Diagnóstico')
    treatment = fields.Text(string='Tratamiento')
    
    @api.depends('date', 'duration')
    def _compute_end_date(self):
        for appointment in self:
            if appointment.date:
                duration_seconds = appointment.duration * 3600
                appointment.end_date = appointment.date + timedelta(seconds=duration_seconds)
            else:
                appointment.end_date = False
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nueva Cita')) == _('Nueva Cita'):
                vals['name'] = self.env['ir.sequence'].next_by_code('cita.medica') or _('Nueva Cita')
        return super(CitaMedica, self).create(vals_list)
    
    def action_confirm(self):
        for appointment in self:
            appointment.state = 'confirmed'
    
    def action_done(self):
        for appointment in self:
            appointment.state = 'done'
    
    def action_cancel(self):
        for appointment in self:
            appointment.state = 'cancelled'
    
    def action_draft(self):
        for appointment in self:
            appointment.state = 'draft'
    
    @api.constrains('date')
    def _check_date(self):
        for appointment in self:
            if appointment.date and appointment.date < fields.Datetime.now():
                raise ValidationError(_("No puedes crear citas en el pasado."))
    
    @api.constrains('date', 'doctor_id')
    def _check_doctor_availability(self):
        for appointment in self:
            if appointment.date and appointment.doctor_id:
                # Buscar citas que se solapen con la misma fecha y médico
                domain = [
                    ('id', '!=', appointment.id),
                    ('doctor_id', '=', appointment.doctor_id.id),
                    ('state', 'in', ['draft', 'confirmed']),
                    ('date', '<=', appointment.end_date),
                    ('end_date', '>=', appointment.date)
                ]
                overlapping = self.search_count(domain)
                if overlapping:
                    raise ValidationError(_("El médico ya tiene una cita programada en este horario."))

