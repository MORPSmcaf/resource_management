{
    'name': "Resource Reservation",
    'summary': "Resource management a platform for managing resources",
    'version': '16.0.1.0.0',
    'website': "https://mcaf.nb.ca/en/",
    'author': "MCAF",
    'category': "Appointments",
    'license': 'OPL-1',
    "application": True,
    "installable": True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/resource_reservation_views.xml',
        'views/resource_reservation_tag_views.xml',
        'views/resource_details_views.xml',
        'views/resource_availability.xml',
        'views/menu.xml',
        'report/detail.xml',
        'data/reservation_tag_data.xml',
        'data/resource_type_data.xml',
        'data/resource_detail_data.xml',
        'data/resource_reservation_data.xml',

    ],
    'demo': [
        'demo/demo.xml',
    ],
}
