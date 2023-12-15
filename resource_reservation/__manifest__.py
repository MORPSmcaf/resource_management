{
    'name': "Resource Reservation",
    'summary': "Resource management platform for managing resources",
    'version': '16.0.1.0.0',
    'website': "https://mcaf.nb.ca/en/",
    'author': "MCAF",
    'category': "Appointments",
    'license': 'OPL-1',
    "application": True,
    "installable": True,
    'depends': ['base', 'mail'],
    'data': [
        'security/resource_reservation_groups.xml',
        'security/ir.model.access.csv',
        'security/resource_reservation_security.xml',
        'views/resource_reservation.xml',
        'views/resource_reservation_views.xml',
        'views/resource_reservation_tag_views.xml',
        'views/resource_views.xml',
        'views/resource_availability.xml',
        'views/menu.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/resource_reservation/static/src/js/resource_button.js',
            '/resource_reservation/static/src/xml/resource_button.xml',
        ]
    },
    'demo': [
        'demo/demo.xml',
    ],
}
