# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MedicalPatient(models.Model):
    _name = 'medical.patient'
    _description = 'Paciente Médico'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Nombre', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Contacto', required=True, 
                                ondelete='cascade', domain=[('is_patient', '=', True)])
    profile_id = fields.Many2one('user.profile', string='Perfil de Usuario', tracking=True)
    
    active = fields.Boolean(default=True, tracking=True)
    
    # Campos relacionados con el partner
    email = fields.Char(related='partner_id.email', string='Email', readonly=False)
    phone = fields.Char(related='partner_id.phone', string='Teléfono', readonly=False)
    
    # Campos médicos relacionados
    medical_history = fields.Text(related='partner_id.medical_history', string='Historial Médico', readonly=False)
    allergies = fields.Text(related='partner_id.allergies', string='Alergias', readonly=False)
    medications = fields.Text(related='partner_id.medications', string='Medicamentos', readonly=False)
    blood_type = fields.Selection(related='partner_id.blood_type', string='Grupo Sanguíneo', readonly=False)
    
    # Citas médicas
    # appointment_ids = fields.One2many('cita.medica', 'partner_id', string='Citas')
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Número de Citas')
    
    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     for patient in self:
    #         patient.appointment_count = len(patient.appointment_ids)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Si se crea un paciente, marcar el partner como paciente
            if vals.get('partner_id'):
                self.env['res.partner'].browse(vals['partner_id']).write({'is_patient': True})
        return super(MedicalPatient, self).create(vals_list)
    
    def write(self, vals):
        # Si se cambia el partner, actualizar los flags
        if 'partner_id' in vals:
            for patient in self:
                if patient.partner_id:
                    patient.partner_id.write({'is_patient': False})
            self.env['res.partner'].browse(vals['partner_id']).write({'is_patient': True})
        return super(MedicalPatient, self).write(vals)
    
    def unlink(self):
        for patient in self:
            if patient.partner_id:
                patient.partner_id.write({'is_patient': False})
        return super(MedicalPatient, self).unlink()
    
    def action_view_appointments(self):
        self.ensure_one()
        return {
            'name': _('Citas'),
            'type': 'ir.actions.act_window',
            'res_model': 'cita.medica',
            'view_mode': 'list,form,calendar',
            'domain': [('partner_id', '=', self.partner_id.id)],
            'context': {'default_partner_id': self.partner_id.id},
        }
