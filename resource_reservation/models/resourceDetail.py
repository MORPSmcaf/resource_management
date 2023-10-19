from odoo import models, fields, api

class ResourceDetail(models.Model):
    _name = 'resource.detail'
    _description = 'Resource Detail'

    resource_name = fields.Char(string='Resource name', required=True)
    resource_type = fields.Char(string='Resource type', required=True)
    resource_capacity = fields.Float(string=" Resource Capacity", required=True)
    resource_owner = fields.Char(string='Resource owner', required=True)
