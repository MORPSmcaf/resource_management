"""Required import for the functionality"""
from odoo import models, fields, api, exceptions, _


class ReservationTag(models.Model):
    """
    This class allows admin users to create a
    reservation tag, edit it, and remove it.
    This reservation tag has been linked
    inside the resource reservation class as well.
    """
    _name = 'resource.reservation.tag'
    _description = 'Reservation Tag'

    name = fields.Char(string='Reservation Type', required=True)
    description = fields.Text(string='Description ')

    _sql_constraints = [
        ('unique_reservation_tag', 'UNIQUE (name)',
         'A reservation tag with the same type already exists.'),
    ]


# Base model is called resource.reservation
class ResourceReservation(models.Model):
    """
    This class represents a resource
    reservation. Allows admin user to
    create reservation
    """
    _name = 'resource.reservation'
    _description = 'Resource Reservation'

    title = fields.Char(string='Title ', required=True)
    name = fields.Many2one('resource.detail',
                           string="Resource Name", required=True)
    start_datetime = fields.Datetime(string='Start Date & Time',
                                     default=lambda self:
                                     fields.Datetime.now(),
                                     help="Store the "
                                          "current date and time",
                                     required=True)
    end_datetime = fields.Datetime(string='End Date & Time',
                                   help="This field will store "
                                        "the end date and time "
                                        "of the event or task.",
                                   required=True)
    creator = fields.Char(string='Created By',
                          default=lambda self: self.env.user.name,
                          required=True)
    booking_status = fields.Selection([
        ('pending', 'Pending '),
        ('confirmed', 'Confirmed '),
        ('canceled', 'Canceled '),
    ],
        string='Booking Status ',
        default='pending',
        help="This field represents the status of the booking.")
    resource_description = fields.Text(string="Reservation Description",
                                       required=True)

    reservation_tag_id = fields.Many2one(
        'resource.reservation.tag',
        string="Reservation Tag", required=True)
    resource_type_id = fields.Many2one(
        'resource.type',
        string="Resource Type", required=True)


    session_ids = fields.One2many(
        'resource.reservation',
        'name',
        string="Sessions")

    def update_booking_status_cancel(self):
        self.write({'booking_status': 'canceled'})

    def update_booking_status_confirm(self):
        self.write({'booking_status': 'confirmed'})

    @api.model
    def create(self, vals_list):
        """Fetches information of current user from odoo environment"""
        vals_list['creator'] = self.env.user.name
        return super().create(vals_list)

    @api.constrains('name', 'start_datetime', 'end_datetime')
    def check_overlapping_reservations(self):
        """Check for overlapping reservations."""
        for reservation in self:
            overlapping = (self.env['resource.reservation'].search([
                # Exclude the current reservation
                ('id', '!=', reservation.id),
                ('name', '=', reservation.name.id),
                ('start_datetime', '<', reservation.end_datetime),
                ('end_datetime', '>', reservation.start_datetime),
            ]))
            if overlapping:
                raise exceptions.ValidationError(_("Overlapping reservations"
                                                   " are not allowed."))

    @api.constrains('start_datetime', 'end_datetime')
    def check_start_end_dates(self):
        """Check that end date is after or equal to start date."""
        for reservation in self:
            if reservation.start_datetime and reservation.end_datetime:
                if reservation.end_datetime < reservation.start_datetime:
                    raise exceptions.ValidationError(_("End date cannot"
                                                       " be before the"
                                                       " start date."))
