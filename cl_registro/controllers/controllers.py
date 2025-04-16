# -*- coding: utf-8 -*-
# from odoo import http


# class ClRegistro(http.Controller):
#     @http.route('/cl_registro/cl_registro', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cl_registro/cl_registro/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cl_registro.listing', {
#             'root': '/cl_registro/cl_registro',
#             'objects': http.request.env['cl_registro.cl_registro'].search([]),
#         })

#     @http.route('/cl_registro/cl_registro/objects/<model("cl_registro.cl_registro"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cl_registro.object', {
#             'object': obj
#         })

