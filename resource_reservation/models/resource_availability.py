# from odoo import models, fields, api
#
#
# class ResourceAvailability(models.Model):
#     _name = 'resource.availability'
#     _description = 'Resource Availability'
#
#     resource_id = fields.Many2one('resource.detail', string="Resource", required=True)
#     start_datetime = fields.Datetime(string='Start Date & Time', required=True)
#     end_datetime = fields.Datetime(string='End Date & Time', required=True)
#     reservation_tag_id = fields.Many2one('resource.reservation.tag',
#                                          string="Reservation Tag", required=True)
#
#     def search_reservations(self):
#         """Search for reservations within the availability period for the resource."""
#         # Perform a search for reservations that overlap with the availability period
#         reservations = self.env['resource.reservation'].search([
#             ('name', '=', self.resource_id.id),
#             ('start_datetime', '<=', self.end_datetime),
#             ('end_datetime', '>=', self.start_datetime)
#         ])
#         return {
#             'name': 'Reservations for Resource',
#             'view_mode': 'tree,form',
#             'res_model': 'resource.reservation',
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', reservations.ids)],
#         }


from odoo import models, fields, api


class ResourceAvailability(models.Model):
    _name = 'resource.availability'
    _description = 'Resource Availability'

    resource_id = fields.Many2one('resource.detail', string="Resource", required=True)
    start_datetime = fields.Datetime(string='Start Date & Time', required=True)
    end_datetime = fields.Datetime(string='End Date & Time', required=True)
    availability_status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Not Available'),
    ], string='Availability Status', compute='_compute_availability_status', store=True)

    @api.depends('resource_id', 'start_datetime', 'end_datetime')
    def _compute_availability_status(self):
        for availability in self:
            reservations = self.env['resource.reservation'].search([
                ('name', '=', availability.resource_id.id),
                ('start_datetime', '<', availability.end_datetime),
                ('end_datetime', '>', availability.start_datetime),
            ])
            if reservations:
                availability.availability_status = 'booked'
            else:
                availability.availability_status = 'available'

    def search_availability(self):
        """Search for resource availability based on resource name, start date, and end date."""
        availability = self.search([
            ('resource_id', '=', self.resource_id.id),
            ('start_datetime', '=', self.start_datetime),
            ('end_datetime', '=', self.end_datetime),
        ])
        return availability
