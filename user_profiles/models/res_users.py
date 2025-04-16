# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    profile_ids = fields.One2many('user.profile', 'user_id', string='Profiles')
    active_profile_id = fields.Many2one('user.profile', string='Active Profile')
    
    # Update security groups references
    @api.onchange('active_profile_id')
    def _onchange_active_profile(self):
        if self.active_profile_id:
            profile_type = self.active_profile_id.profile_type
            
            # Remove existing groups
            groups_to_remove = [
                self.env.ref('medical_partner.group_medical_user').id,
                self.env.ref('medical_partner.group_medical_manager').id,
            ]
            
            # Add appropriate groups based on profile type
            if profile_type == 'doctor':
                self.groups_id = [(3, group_id) for group_id in groups_to_remove]
                self.groups_id = [(4, self.env.ref('medical_partner.group_medical_user').id)]
            elif profile_type == 'admin':
                self.groups_id = [(3, group_id) for group_id in groups_to_remove]
                self.groups_id = [(4, self.env.ref('medical_partner.group_medical_manager').id)]
    
    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'active_profile_id' in vals:
            # Update user's groups based on profile
            for user in self:
                if user.active_profile_id:
                    profile_type = user.active_profile_id.profile_type
                    
                    # Remove existing groups
                    groups_to_remove = [
                        self.env.ref('medical_partner.group_medical_user').id,
                        self.env.ref('medical_partner.group_medical_manager').id,
                    ]
                    
                    # Add appropriate groups based on profile type
                    if profile_type == 'doctor':
                        user.groups_id = [(3, group_id) for group_id in groups_to_remove]
                        user.groups_id = [(4, self.env.ref('medical_partner.group_medical_user').id)]
                    elif profile_type == 'admin':
                        user.groups_id = [(3, group_id) for group_id in groups_to_remove]
                        user.groups_id = [(4, self.env.ref('medical_partner.group_medical_manager').id)]
        return res
    
    @api.model
    def create(self, vals):
        user = super(ResUsers, self).create(vals)
        # Create default profile if needed
        if not user.profile_ids:
            profile_vals = {
                'name': user.name,
                'user_id': user.id,
                'partner_id': user.partner_id.id,
                'profile_type': 'patient',  # Default profile type
            }
            profile = self.env['user.profile'].create(profile_vals)
            user.active_profile_id = profile.id
        return user
    
    def action_create_profile(self):
        self.ensure_one()
        return {
            'name': _('Create Profile'),
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.create.profile',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_user_id': self.id},
        }

