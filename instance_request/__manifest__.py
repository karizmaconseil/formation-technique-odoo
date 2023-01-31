# -*- coding: utf-8 -*-
{
    'name': "Demande d'instance",

    'summary': """
       - Demande de creation dinstance
       - Traiter les flux de creation
       - Alerte les utilisateurs dans la validation de leur besoin
     """,

    'description': """
        -Demande de creation 
          - Groupe utilisateur
          - Aller sur le menu ...
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/instance_request.xml',
        'datas/version_odoo.xml'
    ],
}
