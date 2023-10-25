"""Required import for the functionality"""
from odoo import models, fields, api, exceptions


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
                                     help="Store the current date and time")
    end_datetime = fields.Datetime(string='End Date & Time',
                                   help="This field will store "
                                        "the end date and time "
                                        "of the event or task.")
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
    # res_tag = fields.Char(string="Reservation Tag", required=True)
    reservation_tag_id = fields.Many2one('resource.reservation.tag',
                                      string="Reservation Tag", required=True)

    @api.model
    def create(self, vals_list):
        """Fetches information of current user from odoo environment"""
        vals_list['creator'] = self.env.user.name
        return super().create(vals_list)

    @api.constrains('name', 'start_datetime', 'end_datetime')
    def check_overlapping_reservations(self):
        """Check for overlapping reservations."""
        for reservation in self:
            overlapping_reservations = self.env['resource.reservation'].search([
                ('id', '!=', reservation.id),  # Exclude the current reservation
                ('name', '=', reservation.name.id),
                ('start_datetime', '<', reservation.end_datetime),
                ('end_datetime', '>', reservation.start_datetime),
            ])
            if overlapping_reservations:
                raise exceptions.ValidationError("Overlapping reservations are not allowed.")


    def show_reservation(self):
        # Create a new staff member in the 'mcaf.management.staff' model
        staff_model = self.env['resource.reservation']
        staff_model.create({
            'title': self.title,
            'name' : self.name,
            'start_datetime' : self.start_datetime,
            'end_datetime' : self.end_datetime,
            'creator' : self.creator,
            'resource_description' : self.resource_description,
            'reservation_tag_id' : self.reservation_tag_id,
        })
        return {'type': 'ir.actions.act_window_close'}
