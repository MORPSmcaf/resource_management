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
        'views/resource_reservation_views.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
