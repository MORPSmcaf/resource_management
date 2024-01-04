{
    'name': "Resource Reservation",
    'summary': "Resource management platform for managing resources",
    'version': '16.0.1.3.0',
    'website': "https://mcaf.nb.ca/en/",
    'author': "MCAF",
    'category': "Appointments",
    'license': 'OPL-1',
    "application": True,
    "installable": True,
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/resource_reservation_groups.xml',
        'security/ir.model.access.csv',
        'security/resource_reservation_security.xml',
        'data/resource_reservation_email_template.xml',
        'views/resource_reservation_views.xml',
        'views/resource_reservation_tag_views.xml',
        'views/resource_views.xml',
        'views/resource_availability.xml',
        'views/menu.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
