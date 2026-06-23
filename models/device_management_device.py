# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class DeviceManagementDevice(models.Model):
    _name = 'device.management.device'
    _description = 'Device Management - Device'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _sql_constraints = [
        ('asset_code_unique', 'UNIQUE(asset_code)', 'Asset Code must be unique!'),
    ]

    # ─── General Information ────────────────────────────────────────────────────

    name = fields.Char(
        string='Device Name',
        required=True,
        tracking=True,
        help='Name of the device',
    )

    asset_code = fields.Char(
        string='Asset Code',
        index=True,
        copy=False,
        tracking=True,
        help='Unique asset code or inventory tag for this device',
    )

    def _default_department_id(self):
        return self.env.ref('device_management.dep_not_linked_yet', raise_if_not_found=False)

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        tracking=True,
        default=_default_department_id,
        help='Department that owns this device',
    )

    user_name = fields.Char(
        string='User Name',
        tracking=True,
        help='Operating system user name of the device',
    )

    password = fields.Char(
        string='Password',
        help='Login password for the device',
    )

    location = fields.Char(
        string='Location',
        tracking=True,
        help='Physical location of the device',
    )

    notes = fields.Text(
        string='Notes',
        help='General notes about the device',
    )

    status = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('broken', 'Broken'),
            ('in_repair', 'In Repair'),
            ('retired', 'Retired'),
            ('disposed', 'Disposed'),
            ('parted_out', 'Parted Out'),
        ],
        string='Status',
        default='active',
        tracking=True,
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, the device will be archived',
    )

    # ─── Network ────────────────────────────────────────────────────────────────

    ip_address = fields.Char(
        string='IP Address',
        tracking=True,
        help='IPv4 or IPv6 address of the device',
    )

    mac_address = fields.Char(
        string='MAC Address',
        tracking=True,
        help='MAC address of the device network interface',
    )

    # ─── Operating System ───────────────────────────────────────────────────────

    operating_system = fields.Selection(
        selection=[
            ('windows', 'Windows'),
            ('linux', 'Linux'),
            ('mac', 'Mac'),
            ('others', 'Others'),
        ],
        string='Operating System',
        tracking=True,
    )

    operating_system_series = fields.Char(
        string='OS Series',
        help='E.g. Windows 11, Ubuntu 24.04, Linux Mint 21',
    )

    serial_number = fields.Char(
        string='Serial Number',
        help='OS or device serial number',
    )

    # ─── Specifications ───────────────────────────────────────────────────────────

    processor = fields.Char(
        string='Processor',
        help='Processor model, e.g. Intel Core i7-12700, AMD Ryzen 5 5600X',
    )

    memory_gb = fields.Float(
        string='Memory (GB)',
        help='Total RAM in Gigabytes',
    )

    storage_gb = fields.Float(
        string='Storage (GB)',
        help='Total storage capacity in Gigabytes',
    )

    video_adapter = fields.Char(
        string='Video Adapter',
        help='Graphics card model, e.g. NVIDIA GeForce RTX 3060, Intel UHD Graphics',
    )

    # ─── Device Classification ──────────────────────────────────────────────────

    usage_type = fields.Selection(
        selection=[
            ('workstation', 'Workstation'),
            ('server', 'Server'),
        ],
        string='Usage Type',
        tracking=True,
    )

    device_type = fields.Selection(
        selection=[
            ('pc', 'PC'),
            ('laptop', 'Laptop'),
            ('server', 'Server'),
            ('virtual', 'Virtual'),
            ('embedded', 'Embedded'),
            ('nvr_dvr', 'NVR/DVR'),
            ('camera', 'Camera'),
            ('others', 'Others'),
        ],
        string='Device Type',
        tracking=True,
    )

    # ─── Remote Access ──────────────────────────────────────────────────────────

    remote_type = fields.Selection(
        selection=[
            ('ssh', 'SSH'),
            ('rustdesk', 'RustDesk'),
            ('vnc', 'VNC'),
            ('http', 'HTTP'),
            ('https', 'HTTPS'),
        ],
        string='Remote Type',
        tracking=True,
    )

    remote_id = fields.Char(
        string='Remote ID',
        help='Remote session ID (used for RustDesk)',
    )

    remote_port = fields.Char(
        string='Remote Port',
        help='Port number for remote connection (e.g. 22 for SSH, 5900 for VNC, 80 for HTTP, 443 for HTTPS)',
    )

    remote_url = fields.Char(
        string='Remote URL',
        compute='_compute_remote_url',
        store=False,
        help='Auto-generated URL for one-click remote access',
    )

    remote_command = fields.Char(
        string='Remote Command',
        compute='_compute_remote_url',
        store=False,
        help='Fallback command if URL protocol handler is not registered',
    )

    # ─── Log Relationships ──────────────────────────────────────────────────────

    log_ids = fields.One2many(
        'device.management.log',
        'device_id',
        string='Device Logs',
    )

    log_count = fields.Integer(
        string='Log Count',
        compute='_compute_log_count',
    )

    maintenance_log_ids = fields.One2many(
        'device.management.log',
        'device_id',
        string='Maintenance History',
        domain=[('log_type', '=', 'maintenance')],
    )

    repair_log_ids = fields.One2many(
        'device.management.log',
        'device_id',
        string='Repair Log',
        domain=[('log_type', '=', 'repair')],
    )

    # ─── Computed Methods ────────────────────────────────────────────────────────

    @api.depends('remote_type', 'user_name', 'ip_address', 'remote_id', 'remote_port')
    def _compute_remote_url(self):
        for record in self:
            url = False
            command = False
            port = record.remote_port.strip() if record.remote_port else ''

            if record.remote_type == 'ssh':
                if record.user_name and record.ip_address:
                    base_url = f'{record.user_name}@{record.ip_address}'
                    base_cmd = f'{record.user_name}@{record.ip_address}'
                elif record.ip_address:
                    base_url = record.ip_address
                    base_cmd = record.ip_address
                else:
                    base_url = ''
                    base_cmd = ''
                if base_url:
                    url = f'ssh://{base_url}'
                    command = f'ssh {base_cmd}'
                    if port:
                        url = f'ssh://{base_url}:{port}'
                        command = f'ssh -p {port} {base_cmd}'
            elif record.remote_type == 'rustdesk':
                if record.remote_id:
                    url = f'rustdesk://{record.remote_id}'
                    command = f'rustdesk --connect {record.remote_id}'
                    if port:
                        command = f'rustdesk --connect {record.remote_id}:{port}'
            elif record.remote_type == 'vnc':
                if record.user_name and record.ip_address:
                    base_url = f'{record.user_name}@{record.ip_address}'
                    base_cmd = f'{record.user_name}@{record.ip_address}'
                elif record.ip_address:
                    base_url = record.ip_address
                    base_cmd = record.ip_address
                else:
                    base_url = ''
                    base_cmd = ''
                if base_url:
                    url = f'vnc://{base_url}'
                    command = f'vncviewer {base_cmd}'
                    if port:
                        url = f'vnc://{base_url}:{port}'
                        command = f'vncviewer {base_cmd}:{port}'
            elif record.remote_type == 'http':
                if record.ip_address:
                    url = f'http://{record.ip_address}'
                    command = f'open http://{record.ip_address}'
                    if port:
                        url = f'http://{record.ip_address}:{port}'
                        command = f'open http://{record.ip_address}:{port}'
            elif record.remote_type == 'https':
                if record.ip_address:
                    url = f'https://{record.ip_address}'
                    command = f'open https://{record.ip_address}'
                    if port:
                        url = f'https://{record.ip_address}:{port}'
                        command = f'open https://{record.ip_address}:{port}'
            record.remote_url = url
            record.remote_command = command

    @api.depends('log_ids')
    def _compute_log_count(self):
        for record in self:
            record.log_count = len(record.log_ids)

    # ─── Validation ─────────────────────────────────────────────────────────────

    @api.constrains('ip_address')
    def _check_ip_address(self):
        ipv4_pattern = re.compile(
            r'^(\d{1,3}\.){3}\d{1,3}$'
        )
        ipv6_pattern = re.compile(
            r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$'
        )
        for record in self:
            if record.ip_address:
                ip = record.ip_address.strip()
                if not (ipv4_pattern.match(ip) or ipv6_pattern.match(ip)):
                    raise ValidationError(
                        _('Invalid IP Address format: %s') % ip
                    )

    # ─── Actions ─────────────────────────────────────────────────────────────────

    def action_view_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Device Logs'),
            'res_model': 'device.management.log',
            'view_mode': 'list,form',
            'domain': [('device_id', '=', self.id)],
            'context': {
                'default_device_id': self.id,
            },
        }

    def action_add_log(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Add Log'),
            'res_model': 'device.management.log',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_device_id': self.id,
                'default_user_id': self.env.uid,
            },
        }

    def action_connect_remote(self):
        """Open remote URL using custom URL protocol."""
        self.ensure_one()
        if self.remote_url:
            return {
                'type': 'ir.actions.act_url',
                'url': self.remote_url,
                'target': 'new',
            }
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Remote Access'),
                'message': _('No remote URL configured. Please set the remote type and required fields.'),
                'type': 'warning',
                'sticky': False,
            },
        }
