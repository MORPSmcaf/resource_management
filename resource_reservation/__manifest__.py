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
    'depends': ['base'],
    'data': [
        'security/resource_reservation_groups.xml',
        'security/ir.model.access.csv',
        'security/resource_reservation_rules.xml',
        'security/resource_reservation_security.xml',
        'views/resource_reservation_views.xml',
        'views/resource_reservation_tag_views.xml',
        'views/resource_views.xml',
        'views/resource_availability.xml',
        'views/resource_report.xml',
        'views/menu.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
