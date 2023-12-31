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
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string=' Reservation Tag ', required=True)
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
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Resource Reservation'

    title = fields.Char(string='Title ', required=True)
    resource_name = fields.Many2one(
        'resource',
        string='Resource',
        required=True,
        options={'no_create': True})
    resource_type = fields.Many2one(
        'resource.type',
        string=' Resource Type ',
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
    current_user = fields.Integer(string='User ID',
                                  default=lambda self: self.env.user.id,
                                  required=True)

    name = fields.Char(
        string='Created By',
        readonly=True,
        compute='_compute_created_by_name',
        store=True,
        help="Name of the user who created reservation."
    )

    activity_ids = fields.One2many(
        'mail.activity',
        'res_id',
        string='Activities',
        index=True,
        domain=lambda self: [('res_model', '=', self._name)])

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

    created_by_email = fields.Char(
        string='Created By Email ',
        compute='_compute_created_by_email',
        store=True,
        help="Email of the user who created the reservation."
    )

    @api.depends('create_uid')
    def _compute_created_by_email(self):
        for reservation in self:
            reservation.created_by_email = reservation.create_uid.email

    @api.depends('create_uid')
    def _compute_created_by_name(self):
        for reservation in self:
            reservation.name = reservation.create_uid.name

    def send_confirmation_email(self):
        self.ensure_one()
        template_id = self.env.ref('resource_reservation.test_email_template')
        template_id.send_mail(self.id, force_send=True)

    def update_booking_status_cancel(self):
        for reservation in self:
            if reservation.resource_name.resource_owner.id == self.env.user.id:
                self.write({'booking_status': 'cancelled'})
                reservation.send_confirmation_email()
            else:
                raise exceptions.ValidationError(_("You are not "
                                                   "resource owner"
                                                   " for "
                                                   "this reservation"))

    def update_booking_status_confirm(self):
        for reservation in self:
            if reservation.resource_name.resource_owner.id == self.env.user.id:
                reservation.write({'booking_status': 'confirmed'})
                reservation.send_confirmation_email()
            else:
                raise exceptions.ValidationError(_("You are not "
                                                   "resource owner"
                                                   " for "
                                                   "this reservation"))

    @api.model
    def create(self, vals_list):
        vals_list['create_uid'] = self.env.user.name
        return super().create(vals_list)

    @api.constrains('name', 'start_datetime', 'end_datetime')
    def check_overlapping_reservations(self):
        for reservation in self:
            overlapping = (self.env['resource.reservation'].search([
                ('id', '!=', reservation.id),
                ('resource_name', '=', reservation.resource_name.id),
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

    @api.onchange('resource_name')
    def _onchange_name(self):
        if self.resource_name:
            self.resource_type = self.resource_name.resource_type.id
            return {'domain': {'resource_type': [('id', '=', self.resource_name.resource_type.id)]}}
        else:
            self.resource_type = False
            return {'domain': {'resource_type': []}}

    @api.onchange('resource_type')
    def _onchange_resource_type(self):
        if self.resource_type:
            resource = self.env['resource'].sudo().search(
                [('resource_type', '=', self.resource_type.id)], limit=1)
            self.resource_name = resource
            return {'domain': {'resource_name': [('resource_type', '=', self.resource_type.id)]}}
        else:
            self.resource_name = False
            return {'domain': {'resource_name': []}}

    def write(self, vals):
        if not self.env.user.has_group('resource_reservation.'
                                       'group_resource_reservation_admin'):
            try:
                is_approver = self.env.user.has_group('resource_reservation.'
                                                      'group_resource_'
                                                      'reservation_approver')

                if is_approver and 'booking_status' in vals:
                    return super(ResourceReservation, self).write(vals)

                if 'create_uid' in self and self.create_uid.id != self.env.user.id:
                    raise exceptions.ValidationError(
                        _("Oops! It seems like you're "
                          "trying to access a reservation "
                          "that wasn't created under your "
                          "account. This reservation belongs"
                          " to another user, and you currently"
                          " don't have the "
                          "necessary permissions to modify it"))
                else:
                    return super(ResourceReservation, self).write(vals)

            except exceptions.ValidationError as e:
                raise exceptions.UserError(str(e))
        else:
            return super(ResourceReservation, self).write(vals)

    def unlink(self):
        for reservation in self:
            if not (
                self.env.user.has_group('resource_reservation.'
                                        'group_resource_reservation_admin') or
                reservation.resource_name.resource_owner.id == self.env.user.id
            ):
                raise exceptions.AccessError(_("You do not have the "
                                               "permission to "
                                               "delete this "
                                               "reservation. "
                                               "Only the resource"
                                               " owner or users "
                                               "with 'Admin' access"
                                               " can delete it."))
        return super(ResourceReservation, self).unlink()
