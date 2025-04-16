# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    profile_ids = fields.One2many('user.profile', 'partner_id', string='Profiles')
