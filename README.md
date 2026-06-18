# Device Management

**Language:** [🇬🇧 English](README.md) | [🇮🇩 Indonesia](README-id.md)

Odoo 19 addon for IT company device inventory and management (PC, Laptop, Server, Embedded Device).

## Features

- **Device Master Data**: Records name, department, user, IP, MAC, OS, serial number, device type, and location.
- **Device Log**: Records maintenance, repair, upgrade, and troubleshooting history.
- **One-click Remote Access**: SSH, RustDesk, and VNC support via Custom URL Protocol.
- **Multi Language**: English (en_US) and Indonesian (id_ID).
- **Security Groups**: Device User (read-only), Device Manager (CRUD), Device Administrator (full access).

## Installation

1. Copy this folder to your Odoo addons directory:

```bash
cp -r device_management /path/to/odoo/addons/
```

2. Restart Odoo service:

```bash
sudo systemctl restart odoo
# or
sudo service odoo restart
```

3. Open Odoo, enable *Developer Mode* (Settings → Activate Developer Mode).

4. Go to **Apps → Update Apps List**.

5. Search for **Device Management**, then click **Install**.

### Alternative via Git Clone

```bash
cd /path/to/odoo/addons
git clone <repo-url> device_management
```

Proceed to steps 2-5 above.
