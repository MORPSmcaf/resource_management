# -*- coding: utf-8 -*-
# from odoo import http


# class ResourceManagement(http.Controller):
#     @http.route('/resource_management/resource_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/resource_management/resource_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('resource_management.listing', {
#             'root': '/resource_management/resource_management',
#             'objects': http.request.env['resource_management.resource_management'].search([]),
#         })

#     @http.route('/resource_management/resource_management/objects/<model("resource_management.resource_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('resource_management.object', {
#             'object': obj
#         })
