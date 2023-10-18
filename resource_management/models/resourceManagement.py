from odoo import models, fields


# Our base model is called resource.management
class ResourceManagement(models.Model):
    _name = 'resource.management'
    _description = 'Resource Management'

    title = fields.Char(string='Title', required=True)
    name = fields.Char(string='Resource Name', required=True)
    start_datetime = fields.Date(string='Start Date & Time', default=lambda self: fields.Datetime.now(),
                                 help="This field will store the current date and time when a record is created.")
    end_datetime = fields.Datetime(string='End Date & Time',
                                   help="This field will store the end date and time of the event or task.")
    creator = fields.Char(string='Created By', required=True)
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



