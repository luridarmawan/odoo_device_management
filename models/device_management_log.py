# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DeviceManagementLog(models.Model):
    _name = 'device.management.log'
    _description = 'Device Management - Log'
    _order = 'date desc'
    _rec_name = 'title'

    device_id = fields.Many2one(
        'device.management.device',
        string='Device',
        required=True,
        ondelete='cascade',
        index=True,
    )

    date = fields.Datetime(
        string='Date',
        required=True,
        default=fields.Datetime.now,
    )

    user_id = fields.Many2one(
        'res.users',
        string='Technician',
        required=True,
        default=lambda self: self.env.user,
    )

    title = fields.Char(
        string='Title',
        required=True,
    )

    description = fields.Text(
        string='Description',
    )

    log_type = fields.Selection(
        selection=[
            ('maintenance', 'Maintenance'),
            ('repair', 'Repair'),
            ('upgrade', 'Upgrade'),
            ('troubleshooting', 'Troubleshooting'),
            ('other', 'Other'),
        ],
        string='Log Type',
        default='maintenance',
        required=True,
    )

    # ─── Computed ────────────────────────────────────────────────────────────────

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        related='device_id.department_id',
        store=True,
        readonly=True,
    )
