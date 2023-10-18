{
    'name': "Resource management",
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
        'views/views.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
