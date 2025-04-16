# -*- coding: utf-8 -*-
# from odoo import http


# class ClStock(http.Controller):
#     @http.route('/cl_stock/cl_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cl_stock/cl_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cl_stock.listing', {
#             'root': '/cl_stock/cl_stock',
#             'objects': http.request.env['cl_stock.cl_stock'].search([]),
#         })

#     @http.route('/cl_stock/cl_stock/objects/<model("cl_stock.cl_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cl_stock.object', {
#             'object': obj
#         })

