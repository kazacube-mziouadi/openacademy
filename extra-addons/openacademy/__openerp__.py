# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """
        Gestion de Formation""",

    'description': """
        Formation Open Academy : 
            - cours de Formations
            - sessions de formations
            - attendees registration
    """,

    'author': "Mziouadi",
    'website': "http://www.kazacube.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'templates.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        'views/session_workflow.xml',
        'views/session_board.xml',
        'report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}