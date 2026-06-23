# -*- coding: utf-8 -*-
{
    'name': 'Device Management',
    'version': '19.0.1.3.1',
    'category': 'Inventory',
    'summary': 'IT Device Inventory and Management',
    'description': """
Device Management
=================
IT company device inventory and management module.

Features:
- Device master data (PC, Laptop, Server, Embedded)
- Maintenance & Repair log history
- One-click remote access (SSH, RustDesk, VNC)
- Multi-language: English & Indonesian
- Role-based access control
    """,
    'author': 'CARIK.id',
    'website': 'https://carik.id',
    'depends': [
        'base',
        'hr',
        'mail',
    ],
    'data': [
        'security/device_management_security.xml',
        'security/ir.model.access.csv',
        'data/device_management_data.xml',
        'views/device_management_device_views.xml',
        'views/device_management_log_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'device_management/static/src/**/*',
        ],
    },
    'i18n': [
        'i18n/en.po',
        'i18n/id.po',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
