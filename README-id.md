# Device Management

**Language:** [🇬🇧 English](README.md) | [🇮🇩 Indonesia](README-id.md)

Addon Odoo 19 untuk inventarisasi dan pengelolaan perangkat IT perusahaan (PC, Laptop, Server, Embedded Device).

Bagian dari proyek [odoo-boilerplate](https://github.com/luridarmawan/odoo-boilerplate) untuk Odoo 19.

## Tangkapan Layar

| Dashboard | Detail Perangkat |
|-----------|------------------|
| ![Dashboard](docs/dashboard.png) | ![Detail Perangkat](docs/detail.png) |

## Fitur

- **Master Data Perangkat**: Pencatatan nama, departemen, user, IP, MAC, OS, serial number, tipe perangkat, dan lokasi.
- **Device Log**: Pencatatan riwayat maintenance, repair, upgrade, dan troubleshooting.
- **One-click Remote Access**: Dukungan SSH, RustDesk, dan VNC via Custom URL Protocol.
- **Multi Language**: English (en_US) dan Bahasa Indonesia (id_ID).
- **Security Groups**: Device User (read-only), Device Manager (CRUD), Device Administrator (full access).

## Multi Bahasa

Modul ini mendukung dua bahasa:

| Bahasa           | Lokal  | Berkas            |
|------------------|--------|-------------------|
| English          | en_US  | `i18n/en.po`      |
| Bahasa Indonesia | id_ID  | `i18n/id.po`      |

Bahasa terdeteksi secara otomatis dari preferensi bahasa pengguna di Odoo.

## Instalasi

### Instalasi Tradisional

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

### Instalasi Docker

Jika Anda menggunakan [odoo-boilerplate](https://github.com/luridarmawan/odoo-boilerplate) dengan Docker:

1. Clone repositori ini ke direktori `addons/`:

```bash
cd /path/to/odoo-boilerplate/addons
git clone <repo-url> device_management
```

2. Restart container Docker:

```bash
docker compose restart
```

3. Buka Odoo, aktifkan *Developer Mode* (Settings → Activate Developer Mode).

4. Masuk ke menu **Apps → Update Apps List**.

5. Cari **Device Management**, lalu klik **Install**.
