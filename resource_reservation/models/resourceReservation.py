from odoo import models, fields, api


class ReservationTag(models.Model):
    _name = 'resource.reservation.tag'
    _description = 'Reservation Tag'

    name = fields.Char(string='Reservation Type', required=True)
    des = fields.Text(string='Description')


# Our base model is called resource.reservation
class ResourceReservation(models.Model):
    _name = 'resource.reservation'
    _description = 'Resource Reservation'

    title = fields.Char(string='Title', required=True)
    name = fields.Char(string='Resource', required=True)
    start_datetime = fields.Datetime(string='Start Date & Time', default=lambda self: fields.Datetime.now(),
                                 help="This field will store the current date and time when a record is created.")
    end_datetime = fields.Datetime(string='End Date & Time',
                                   help="This field will store the end date and time of the event or task.")
    creator = fields.Char(string='Created By', default=lambda self: self.env.user.name, required=True)
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
    res_des = fields.Text(string="Reservation Description", required=True)
    # res_tag = fields.Char(string="Reservation Tag", required=True)
    res_tag_id = fields.Many2one('resource.reservation.tag', string="Resource Tag", required=True)

    @api.model
    def create(self, values):
        values['creator'] = self.env.user.name
        return super(ResourceReservation, self).create(values)
