# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class InicioMedico(models.Model):
    _name = 'inicio.medico'
    _description = 'Médico'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Nombre', required=True, tracking=True)
    partner_id2 = fields.Many2one('res.partner', string='Contacto', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', tracking=True)
    
    specialty = fields.Char(string='Especialidad', tracking=True)
    license_number = fields.Char(string='Número de Licencia', tracking=True)
    
    active = fields.Boolean(default=True, tracking=True)
    
    appointment_ids = fields.One2many('cita.medica', 'doctor_id', string='Citas')
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Número de Citas')
    
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for doctor in self:
            doctor.appointment_count = len(doctor.appointment_ids)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Si se crea un médico, marcar el partner como doctor
            if vals.get('partner_id2'):
                self.env['res.partner'].browse(vals['partner_id2']).write({'is_doctor': True})
        return super(InicioMedico, self).create(vals_list)
    
    def write(self, vals):
        # Si se cambia el partner, actualizar los flags
        if 'partner_id2' in vals:
            for doctor in self:
                if doctor.partner_id2:
                    doctor.partner_id2.write({'is_doctor': False})
            self.env['res.partner'].browse(vals['partner_id2']).write({'is_doctor': True})
        return super(InicioMedico, self).write(vals)
    
    def unlink(self):
        for doctor in self:
            if doctor.partner_id:
                doctor.partner_id.write({'is_doctor': False})
        return super(InicioMedico, self).unlink()
    
    def action_view_appointments(self):
        self.ensure_one()
        return {
            'name': _('Citas'),
            'type': 'ir.actions.act_window',
            'res_model': 'cita.medica',
            'view_mode': 'list,form,calendar',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
        }
