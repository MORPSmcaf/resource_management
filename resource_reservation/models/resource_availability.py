from odoo import models, fields, api, exceptions, _


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
        availability = self.search([
            ('resource_id', '=', self.resource_id.id),
            ('start_datetime', '=', self.start_datetime),
            ('end_datetime', '=', self.end_datetime),
        ])
        if availability.availability_status == 'available':

            return {
                'name': 'Show Reservation',
                'type': 'ir.actions.act_window',
                'res_model': 'resource.reservation',
                'view_mode': 'form',
                'view_id': False,
                'target': 'new',
            }

        else:
            # Resource is not available, display a message
            raise exceptions.UserError("Resource is not available for the selected time period.")

    def check_availability_start_end_date(self):
        if self.start_datetime and self.end_datetime:
            # Get the start and end datetime values
            start_datetime = self.start_datetime
            end_datetime = self.end_datetime

            # Search for available resources during the specified time period
            available_resources = self.env['resource.availability'].search([
                ('start_datetime', '<', end_datetime),
                ('end_datetime', '>', start_datetime),
            ])

            if available_resources:
                # Resources are available, display their details
                available_resource_names = available_resources.mapped('resource_id.name')
                message = f"Available resources: {', '.join(available_resource_names)}"
            else:
                # No resources are available during the specified time period
                message = "No resources are available for the selected time period."

            # Display a message to the user
            return {
                'name': 'Availability Result',
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Resource Availability',
                    'message': message,
                }
            }
        else:
            raise exceptions.UserError("Please provide both start and end dates.")



