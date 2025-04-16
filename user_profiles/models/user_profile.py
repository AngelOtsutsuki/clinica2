# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import re

_logger = logging.getLogger(__name__)

class UserProfile(models.Model):
    _name = 'user.profile'
    _description = 'User Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='User', tracking=True)
    
    # Use security groups from medical_partner module
    profile_type = fields.Selection([
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator')
    ], string='Profile Type', required=True, default='patient', tracking=True,
       groups="medical_partner.group_user_profile_manager")
    
    active = fields.Boolean(default=True, tracking=True)
    email = fields.Char(related='partner_id.email', string='Email', store=True, readonly=False)
    phone = fields.Char(related='partner_id.phone', string='Phone', store=True, readonly=False)
    
    street = fields.Char(related='partner_id.street', string='Street', store=True, readonly=False)
    street2 = fields.Char(related='partner_id.street2', string='Street 2', store=True, readonly=False)
    zip = fields.Char(related='partner_id.zip', string='ZIP', store=True, readonly=False)
    city = fields.Char(related='partner_id.city', string='City', store=True, readonly=False)
    state_id = fields.Many2one(related='partner_id.state_id', string='State', store=True, readonly=False)
    country_id = fields.Many2one(related='partner_id.country_id', string='Country', store=True, readonly=False)
    
    # Campos relacionados con información médica
    medical_history = fields.Text(related='partner_id.medical_history', string='Medical History', 
                                 store=True, readonly=False,
                                 groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    allergies = fields.Text(related='partner_id.allergies', string='Allergies',
                           store=True, readonly=False,
                           groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    medications = fields.Text(related='partner_id.medications', string='Current Medications',
                             store=True, readonly=False,
                             groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    
    # Campos adicionales relacionados
    blood_type = fields.Selection(related='partner_id.blood_type', string='Blood Type',
                                 store=True, readonly=False,
                                 groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    height = fields.Float(related='partner_id.height', string='Height (cm)',
                         store=True, readonly=False,
                         groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    weight = fields.Float(related='partner_id.weight', string='Weight (kg)',
                         store=True, readonly=False,
                         groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    birth_date = fields.Date(related='partner_id.birth_date', string='Birth Date',
                            store=True, readonly=False)
    gender = fields.Selection(related='partner_id.gender', string='Gender',
                             store=True, readonly=False)
    
    # Campos de contacto de emergencia
    emergency_contact = fields.Char(related='partner_id.emergency_contact', string='Emergency Contact',
                                   store=True, readonly=False,
                                   groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    emergency_phone = fields.Char(related='partner_id.emergency_phone', string='Emergency Phone',
                                 store=True, readonly=False,
                                 groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    
    # Campos de seguro médico
    # insurance_provider = fields.Char(related='partner_id.insurance_provider', string='Insurance Provider',
    #                                 store=True, readonly=False,
    #                                 groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    # insurance_policy_number = fields.Char(related='partner_id.insurance_policy_number', string='Policy Number',
    #                                      store=True, readonly=False,
    #                                      groups="medical_partner.group_medical_user,medical_partner.group_medical_manager")
    
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    image_128 = fields.Image("Image (128)", related="image_1920", max_width=128, max_height=128, store=True)
    
    # Relación con medical.patient
    patient_id = fields.Many2one('medical.patient', string='Medical Patient Record')
    
    @api.model
    def create(self, vals):
        res = super(UserProfile, self).create(vals)
        if res.profile_type == 'patient':
            # Update partner as patient
            res.partner_id.write({
                'is_patient': True,
                'is_doctor': False,
            })
            
            # Create patient record if it doesn't exist
            patient = self.env['medical.patient'].search([('partner_id', '=', res.partner_id.id)], limit=1)
            if not patient:
                patient_vals = {
                    'name': res.name,
                    'partner_id': res.partner_id.id,
                    'profile_id': res.id,
                }
                patient = self.env['medical.patient'].create(patient_vals)
                res.patient_id = patient.id
                
        elif res.profile_type == 'doctor':
            # Update partner as doctor
            res.partner_id.write({
                'is_doctor': True,
                'is_patient': False,
            })
            
            # Create doctor record if it doesn't exist
            doctor = self.env['inicio.medico'].search([('partner_id', '=', res.partner_id.id)], limit=1)
            if not doctor:
                doctor_vals = {
                    'name': res.name,
                    'partner_id': res.partner_id.id,
                    'user_id': res.user_id.id if res.user_id else False,
                }
                doctor = self.env['inicio.medico'].create(doctor_vals)
        return res
    
    def write(self, vals):
        res = super(UserProfile, self).write(vals)
        for profile in self:
            if 'profile_type' in vals:
                if vals['profile_type'] == 'patient':
                    # Update partner as patient
                    profile.partner_id.write({
                        'is_patient': True,
                        'is_doctor': False,
                    })
                    
                    # Create patient record if it doesn't exist
                    patient = self.env['medical.patient'].search([('partner_id', '=', profile.partner_id.id)], limit=1)
                    if not patient:
                        patient_vals = {
                            'name': profile.name,
                            'partner_id': profile.partner_id.id,
                            'profile_id': profile.id,
                        }
                        patient = self.env['medical.patient'].create(patient_vals)
                        profile.patient_id = patient.id
                        
                elif vals['profile_type'] == 'doctor':
                    # Update partner as doctor
                    profile.partner_id.write({
                        'is_doctor': True,
                        'is_patient': False,
                    })
                    
                    # Create doctor record if it doesn't exist
                    doctor = self.env['inicio.medico'].search([('partner_id', '=', profile.partner_id.id)], limit=1)
                    if not doctor:
                        doctor_vals = {
                            'name': profile.name,
                            'partner_id': profile.partner_id.id,
                            'user_id': profile.user_id.id if profile.user_id else False,
                        }
                        doctor = self.env['inicio.medico'].create(doctor_vals)
        return res
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError(_("Invalid email format!"))
    
    def action_activate(self):
        self.ensure_one()
        self.active = True
        return True
    
    def action_deactivate(self):
        self.ensure_one()
        self.active = False
        return True
    
    def action_view_appointments(self):
        self.ensure_one()
        return {
            'name': _('Appointments'),
            'type': 'ir.actions.act_window',
            'res_model': 'cita.medica',
            'view_mode': 'list,form,calendar',
            'domain': [('partner_id', '=', self.partner_id.id)],
            'context': {'default_partner_id': self.partner_id.id},
        }



