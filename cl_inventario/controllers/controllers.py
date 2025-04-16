# -*- coding: utf-8 -*-
# from odoo import http


# class ClInventario(http.Controller):
#     @http.route('/cl_inventario/cl_inventario', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cl_inventario/cl_inventario/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cl_inventario.listing', {
#             'root': '/cl_inventario/cl_inventario',
#             'objects': http.request.env['cl_inventario.cl_inventario'].search([]),
#         })

#     @http.route('/cl_inventario/cl_inventario/objects/<model("cl_inventario.cl_inventario"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cl_inventario.object', {
#             'object': obj
#         })

