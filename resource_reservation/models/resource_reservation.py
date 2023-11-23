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
    color_reservation_tag = fields.Integer(string='Color ')

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
    name = fields.Many2one(
        'resource',
        string='Resource Name',
        required=True,
        options={'no_create': True})
    resource_type = fields.Many2one(
        'resource.type',
        string='Resource Type',
        required=True,
        options={'no_create': True})
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
    user_id = fields.Integer(string='User ID',
                             default=lambda self: self.env.user.id,
                             required=True)
    booking_status = fields.Selection([
        ('pending', 'Pending '),
        ('confirmed', 'Confirmed '),
        ('cancelled', 'Cancelled '),
    ],
        string='Booking Status ',
        default='pending',
        help="This field represents the status of the booking.")
    resource_description = fields.Text(string="Reservation Description",
                                       required=True)

    reservation_tag_id = fields.Many2many(
        'resource.reservation.tag',
        string="Reservation Tag",
        required=True,
        widget='many2many_tags')

    color_reserv = fields.Integer(
        string='Color',
        related='resource_type.color_resource_type',
        store=True)

    def update_booking_status_cancel(self):
        self.write({'booking_status': 'cancelled'})

    def update_booking_status_confirm(self):
        self.write({'booking_status': 'confirmed'})

    @api.model
    def create(self, vals_list):
        vals_list['create_uid'] = self.env.user.name
        return super().create(vals_list)

    @api.constrains('name', 'start_datetime', 'end_datetime')
    def check_overlapping_reservations(self):
        for reservation in self:
            overlapping = (self.env['resource.reservation'].search([
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
        for reservation in self:
            if reservation.start_datetime and reservation.end_datetime:
                if reservation.end_datetime < reservation.start_datetime:
                    raise exceptions.ValidationError(_("End date cannot"
                                                       " be before the"
                                                       " start date."))

    @api.constrains('start_datetime')
    def check_future_start_date(self):
        for i in self:
            if i.start_datetime and i.start_datetime < fields.Datetime.now():
                raise exceptions.ValidationError(_("Bookings for "
                                                   "past dates are "
                                                   "not allowed."))

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            return {'domain': {'resource_type': [
                ('id', '=',
                 self.name.resource_type.id), ('id', '!=', False)]}}

    @api.onchange('resource_type')
    def _onchange_resource_type(self):
        if self.resource_type:
            # mb better if it will be in 1 line ?
            self.name = self.env['resource'].search(
                [('resource_type', '=', self.resource_type.id)], limit=1)
            # mb better if it will be in 1 line ?
            return {'domain': {'name': [
                ('resource_type', '=',
                 self.resource_type.id), ('id', '!=', False)]}}
