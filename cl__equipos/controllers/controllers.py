# -*- coding: utf-8 -*-
# from odoo import http


# class ClEquipos(http.Controller):
#     @http.route('/cl__equipos/cl__equipos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cl__equipos/cl__equipos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cl__equipos.listing', {
#             'root': '/cl__equipos/cl__equipos',
#             'objects': http.request.env['cl__equipos.cl__equipos'].search([]),
#         })

#     @http.route('/cl__equipos/cl__equipos/objects/<model("cl__equipos.cl__equipos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cl__equipos.object', {
#             'object': obj
#         })

