# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class WizardCreateProfile(models.TransientModel):
    _name = 'wizard.create.profile'
    _description = 'Create User Profile Wizard'
    
    user_id = fields.Many2one('res.users', string='User', required=True)
    name = fields.Char(string='Profile Name', required=True)
    profile_type = fields.Selection([
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator')
    ], string='Profile Type', required=True, default='patient')
    
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char(string='ZIP')
    country_id = fields.Many2one('res.country', string='Country')
    
    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id:
            self.name = self.user_id.name
            self.email = self.user_id.email
            self.phone = self.user_id.phone
    
    def action_create_profile(self):
        self.ensure_one()
        
        # Check if profile with same type already exists
        existing_profile = self.env['user.profile'].search([
            ('user_id', '=', self.user_id.id),
            ('profile_type', '=', self.profile_type)
        ], limit=1)
        
        if existing_profile:
            raise ValidationError(_("A profile with this type already exists for this user."))
        
        # Create or get partner
        partner = self.user_id.partner_id
        
        # Create profile
        profile_vals = {
            'name': self.name,
            'user_id': self.user_id.id,
            'partner_id': partner.id,
            'profile_type': self.profile_type,
            'email': self.email,
            'phone': self.phone,
        }
        
        profile = self.env['user.profile'].create(profile_vals)
        
        # Update partner address if provided
        address_vals = {}
        if self.street:
            address_vals['street'] = self.street
        if self.street2:
            address_vals['street2'] = self.street2
        if self.city:
            address_vals['city'] = self.city
        if self.state_id:
            address_vals['state_id'] = self.state_id.id
        if self.zip:
            address_vals['zip'] = self.zip
        if self.country_id:
            address_vals['country_id'] = self.country_id.id
        
        if address_vals:
            partner.write(address_vals)
        
        # Set as active profile
        self.user_id.active_profile_id = profile.id
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('User Profile'),
            'res_model': 'user.profile',
            'res_id': profile.id,
            'view_mode': 'form',
            'target': 'current',
        }
