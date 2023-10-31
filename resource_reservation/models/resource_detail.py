"""Its just show what moduls are imported"""
from odoo import models, fields, api


class ResourceDetail(models.Model):
    """ This module create data for Resource Detail fields in odoo
        model resource_reservation"""
    _name = 'resource.detail'
    _description = 'Resource Detail'

    name = fields.Char(string='Resource name', required=True)
    resource_type = fields.Many2one(
        'resource.type',
        string="Resource Type ", required=True)
    resource_capacity = fields.Float(string=" Resource Capacity",
                                     required=True)
    resource_owner = fields.Char(string='Resource owner', required=True)
    image = fields.Binary(string='')
    reservation_ids = fields.One2many('resource.reservation',
                                      'name',
                                      string='Reservations')
    confirmed_reservations = fields.One2many('resource.reservation',
                                             'name',
                                             compute='_compute_confirmed')
    cancelled_reservations = fields.One2many('resource.reservation',
                                             'name',
                                             compute='_compute_cancelled')

    @api.depends('reservation_ids')
    def _compute_confirmed(self):
        for record in self:
            record.confirmed_reservations = record.reservation_ids.filtered(
                lambda r: r.booking_status == 'confirmed')

    @api.depends('reservation_ids')
    def _compute_cancelled(self):
        for record in self:
            record.cancelled_reservations = record.reservation_ids.filtered(
                lambda r: r.booking_status == 'cancelled')


class ResourceType(models.Model):
    _name = 'resource.type'
    _description = 'Resource Type'

    name = fields.Char(string='Resource Type', required=True)

    _sql_constraints = [
        ('unique_resource_type', 'UNIQUE (name)',
         'A resource type with the same name already exists.'),
    ]
