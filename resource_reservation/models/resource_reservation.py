"""Required import for the functionality"""
from odoo import models, fields, api


class ReservationTag(models.Model):
    """
    This class allows admin users to create a reservation tag, edit it, and remove it.
    This reservation tag has been linked inside the resource reservation class as well.
    """
    _name = 'resource.reservation.tag'
    _description = 'Reservation Tag'

    name = fields.Char(string='Reservation Type', required=True)
    description = fields.Text(string='Description')


# Base model is called resource.reservation
class ResourceReservation(models.Model):
    """
    This class represents a resource reservation. Allows admin user to create reservation
    """
    _name = 'resource.reservation'
    _description = 'Resource Reservation'

    title = fields.Char(string='Title', required=True)
    name = fields.Char(string='Resource', required=True)
    start_datetime = fields.Datetime(string='Start Date & Time',
                                     default=lambda self: fields.Datetime.now(),
                                     help="Store the current date and time")
    end_datetime = fields.Datetime(string='End Date & Time', help="This field will store "
                                   "the end date and time of the event or task.")
    creator = fields.Char(string='Created By', default=lambda self: self.env.user.name,
                          required=True)
    booking_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
        ('other', 'Other'),
    ],
        string='Booking Status',
        default='pending',
        help="This field represents the status of the booking.")
    resource_description = fields.Text(string="Reservation Description", required=True)
    # res_tag = fields.Char(string="Reservation Tag", required=True)
    resource_tag_id = fields.Many2one('resource.reservation.tag', string="Resource Tag", required=True)

    # Fetches information of current user from odoo environment
    @api.model
    def create(self, vals_list):
        vals_list['creator'] = self.env.user.name
        return super().create(vals_list)
