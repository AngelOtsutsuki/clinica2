from odoo import http
from odoo.http import request

class MedicalPartner(http.Controller):
    @http.route('/medical_partner/dashboard', auth='user', website=True)
    def dashboard(self, **kw):
        # Obtener el usuario actual
        user = request.env.user
        
        # Verificar si el usuario es un paciente
        is_patient = request.env['res.groups'].search([
            ('id', '=', request.env.ref('user_profiles.group_medical_patient').id),
            ('users', 'in', user.id)
        ])
        
        # Verificar si el usuario es un doctor
        is_doctor = request.env['res.groups'].search([
            ('id', '=', request.env.ref('user_profiles.group_medical_doctor').id),
            ('users', 'in', user.id)
        ])
        
        # Obtener datos según el tipo de usuario
        if is_patient:
            # Obtener el perfil del paciente
            patient_profile = request.env['user.profile'].search([
                ('user_id', '=', user.id),
                ('profile_type', '=', 'patient')
            ], limit=1)
            
            # Obtener el contacto del paciente
            patient = request.env['res.partner'].search([
                ('user_id', '=', user.id),
                ('is_patient', '=', True)
            ], limit=1)
            
            # Obtener las citas del paciente
            appointments = request.env['cita.medica'].search([
                ('patient_id', '=', patient.id)
            ])
            
            return request.render('medical_partner.patient_dashboard_template', {
                'patient': patient,
                'profile': patient_profile,
                'appointments': appointments,
            })
        
        elif is_doctor:
            # Obtener el perfil del doctor
            doctor_profile = request.env['user.profile'].search([
                ('user_id', '=', user.id),
                ('profile_type', '=', 'doctor')
            ], limit=1)
            
            # Obtener el contacto del doctor
            doctor = request.env['res.partner'].search([
                ('user_id', '=', user.id),
                ('is_doctor', '=', True)
            ], limit=1)
            
            # Obtener las citas del doctor
            appointments = request.env['cita.medica'].search([
                ('doctor_id', '=', doctor.id)
            ])
            
            return request.render('medical_partner.doctor_dashboard_template', {
                'doctor': doctor,
                'profile': doctor_profile,
                'appointments': appointments,
            })
        
        else:
            return request.redirect('/web/login')