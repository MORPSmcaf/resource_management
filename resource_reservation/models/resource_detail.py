"""Its just show what moduls are imported"""
from odoo import models, fields


class ResourceDetail(models.Model):
    """ This module create data for Resource Detail fields in odoo
        model resource_reservation"""
    _name = 'resource.detail'
    _description = 'Resource Detail'

    name = fields.Char(string='Resource name', required=True)
    resource_type = fields.Char(string='Resource type', required=True)
    resource_capacity = fields.Float(string=" Resource Capacity",
                                     required=True)
    resource_owner = fields.Char(string='Resource owner', required=True)
