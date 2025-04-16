# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Campos básicos para pacientes
    is_patient = fields.Boolean(string='Es Paciente', default=False)
    is_doctor = fields.Boolean(string='Es Doctor', default=False)
    
    # Campos médicos
    medical_history = fields.Text(string='Historial Médico')
    allergies = fields.Text(string='Alergias')
    medications = fields.Text(string='Medicamentos Actuales')
    
    # Información médica adicional
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string='Grupo Sanguíneo')
    height = fields.Float(string='Altura (cm)')
    weight = fields.Float(string='Peso (kg)')
    
    # Información de contacto de emergencia
    emergency_contact = fields.Char(string='Contacto de Emergencia')
    emergency_phone = fields.Char(string='Teléfono de Emergencia')
    emergency_relationship = fields.Char(string='Relación con Contacto de Emergencia')
    
    # Información médica adicional
    birth_date = fields.Date(string='Fecha de Nacimiento')
    gender = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino'),
        ('other', 'Otro')
    ], string='Género')
    
    # Relaciones con otros modelos médicos
    doctor_id = fields.Many2one('inicio.medico', string='Médico Asignado')
    patient_id = fields.One2many('medical.patient', 'partner_id', string='Pacientes Médicos')
    
    # Historial de citas
    appointment_ids = fields.One2many('cita.medica', 'partner_id3', string='Citas Médicas')
    
    # Campos para estadísticas y seguimiento
    last_appointment_date = fields.Date(string='Fecha de Última Cita', compute='_compute_last_appointment')
    appointment_count = fields.Integer(string='Número de Citas', compute='_compute_appointment_count')
    
    @api.depends('appointment_ids')
    def _compute_last_appointment(self):
        for partner in self:
            appointments = partner.appointment_ids.sorted('date', reverse=True)
            partner.last_appointment_date = appointments[0].date if appointments else False
    
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for partner in self:
            partner.appointment_count = len(partner.appointment_ids)
    
    # Métodos para acciones relacionadas con pacientes
    def action_view_appointments(self):
        self.ensure_one()
        return {
            'name': 'Citas del Paciente',
            'type': 'ir.actions.act_window',
            'res_model': 'cita.medica',
            'view_mode': 'list,form,calendar',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
    
    def action_create_appointment(self):
        self.ensure_one()
        return {
            'name': 'Nueva Cita',
            'type': 'ir.actions.act_window',
            'res_model': 'cita.medica',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_partner_id': self.id},
        }
    
        # Añade este método a tu clase ResPartner en res_partner.py
    def action_view_medical_appointments(self):
        self.ensure_one()
        action = self.env.ref('medical_partner.action_medical_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action

    # También necesitarías añadir un campo para contar las citas
    appointment_count = fields.Integer(string='Citas', compute='_compute_appointment_count')

    def _compute_appointment_count(self):
        for partner in self:
            partner.appointment_count = self.env['medical.appointment'].search_count([
                ('patient_id', '=', partner.id)
            ])
