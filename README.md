# Device Management

Addon Odoo 19 untuk inventarisasi dan pengelolaan perangkat IT perusahaan (PC, Laptop, Server, Embedded Device).

## Fitur

- **Master Data Perangkat**: Pencatatan nama, departemen, user, IP, MAC, OS, serial number, tipe perangkat, dan lokasi.
- **Device Log**: Pencatatan riwayat maintenance, repair, upgrade, dan troubleshooting.
- **One-click Remote Access**: Dukungan SSH, RustDesk, dan VNC via Custom URL Protocol.
- **Multi Language**: English (en_US) dan Bahasa Indonesia (id_ID).
- **Security Groups**: Device User (read-only), Device Manager (CRUD), Device Administrator (full access).

## Instalasi

1. Salin folder ini ke direktori addons Odoo Anda:

```bash
cp -r device_management /path/to/odoo/addons/
```

2. Restart service Odoo:

```bash
sudo systemctl restart odoo
# atau
sudo service odoo restart
```

3. Buka Odoo, aktifkan *Developer Mode* (Settings → Activate Developer Mode).

4. Masuk ke menu **Apps → Update Apps List**.

5. Cari **Device Management**, lalu klik **Install**.

### Alternatif via Git Clone

```bash
cd /path/to/odoo/addons
git clone <repo-url> device_management
```

Lanjutkan ke langkah 2-5 di atas.
