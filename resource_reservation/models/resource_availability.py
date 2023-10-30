from odoo import models, fields, api, exceptions, _


class ResourceAvailability(models.Model):
    _name = 'resource.availability'
    _description = 'Resource Availability'

    resource_id = fields.Many2one('resource.detail',
                                  string="Resource Name",
                                  required=True)
    start_datetime = fields.Datetime(string='Start Date & Time', required=True)
    end_datetime = fields.Datetime(string='End Date & Time', required=True)
    availability_status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Not Available'),
    ], name='Availability Status',
        compute='_compute_availability_status',
        store=True)

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
        # Resource is not available, display a message
        raise exceptions.UserError(_("Resource is not available for"
                                     " the selected time period."))

    @api.constrains('start_datetime', 'end_datetime')
    def check_start_end_dates(self):
        """Check that end date is after or equal to start date."""
        for reservation in self:
            if reservation.start_datetime and reservation.end_datetime:
                if reservation.end_datetime < reservation.start_datetime:
                    raise exceptions.ValidationError(_("End date cannot"
                                                       " be before the"
                                                       " start date."))


class ResourceAvailabilityByResource(models.Model):
    _name = 'resource.availability.by.resource'
    _description = 'Resource Availability By Resource'

    resource_id = fields.Many2one('resource.detail',
                                  string="Resource Name",
                                  required=True)
    related_bookings = fields.Many2many('resource.reservation',
                                        compute='_compute_related_bookings')

    @api.depends('resource_id')
    def _compute_related_bookings(self):
        for i in self:
            i.related_bookings = self.env['resource.reservation'].search([
                ('name', '=', i.resource_id.id),
            ])

    def show_related_bookings(self):
        self.ensure_one()
        return {
            'name': 'Related Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'resource.reservation',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.related_bookings.ids)],
            'target': 'current',
        }


class ResourceAvailabilityByDate(models.Model):
    _name = 'resource.availability.by.dates'
    _description = 'Resource Availability By Date'

    start_date = fields.Datetime(string='Start Date & Time', required=True)
    end_date = fields.Datetime(string='End Date & Time', required=True)
    related_bookings = fields.Many2many('resource.reservation',
                                        compute='_compute_related_bookings')

    @api.depends('start_date', 'end_date')
    def _compute_related_bookings(self):
        for i in self:
            i.related_bookings = self.env['resource.reservation'].search([
                ('start_datetime', '<', i.end_date),
                ('end_datetime', '>', i.start_date),
            ])

    def show_related_bookings(self):
        self.ensure_one()
        return {
            'name': 'Related Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'resource.reservation',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.related_bookings.ids)],
            'target': 'current',
        }

    @api.constrains('start_date', 'end_date')
    def check_start_end_dates(self):
        """Check that end date is after or equal to start date."""
        for reservation in self:
            if reservation.start_date and reservation.end_date:
                if reservation.end_date < reservation.start_date:
                    raise exceptions.ValidationError(_("End date cannot"
                                                       " be before the"
                                                       " start date."))
