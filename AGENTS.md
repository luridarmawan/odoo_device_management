# AGENTS.md

## Project Overview

Project ini adalah addon Odoo bernama **Device Management** yang digunakan untuk inventarisasi dan pengelolaan perangkat IT perusahaan seperti PC, Laptop, Server, dan Embedded Device.

Target utama:

* Inventaris perangkat terpusat.
* Mendukung pencatatan riwayat perbaikan dan maintenance.
* Mendukung kontrol akses berbasis role.
* Mendukung one-click remote access.
* Mendukung multi-language minimal:

  * English (en_US)
  * Bahasa Indonesia (id_ID)

---

## Functional Requirements

### Device Master Data

Buat model utama:

`device.management.device`

Field yang wajib tersedia:

| Field                   | Type                    | Description                                              |
| ----------------------- | ----------------------- | -------------------------------------------------------- |
| name                    | Char                    | Nama perangkat                                           |
| department_id           | Many2one(hr.department) | Departemen pemilik perangkat                             |
| user_name               | Char                    | Nama user perangkat                                      |
| password                | Char                    | Password perangkat                                       |
| ip_address              | Char                    | IPv4/IPv6                                                |
| mac_address             | Char                    | MAC Address                                              |
| operating_system        | Selection               | Windows/Linux/Mac/Others                                 |
| operating_system_series | Char                    | Contoh: Windows 10, Windows 11, Linux Mint, Ubuntu 24.04 |
| serial_number           | Char                    | Serial Number OS atau perangkat                          |
| usage_type              | Selection               | Workstation / Server                                     |
| device_type             | Selection               | PC / Laptop / Server / Embedded                          |
| location                | Char                    | Lokasi perangkat                                         |
| notes                   | Text                    | Catatan umum                                             |
| remote_id               | Char                    | ID remote                                                |
| remote_type             | Selection               | SSH / RustDesk / VNC                                     |
| active                  | Boolean                 | Active/Archived                                          |

Default department:

* "Not Linked Yet" / "Belum Dilinkkan"

---

## Device Log

Buat model:

`device.management.log`

Tujuan:

Mencatat seluruh aktivitas maintenance, repair, upgrade, troubleshooting, dan tindakan lainnya terhadap perangkat.

Field:

| Field       | Type                               |
| ----------- | ---------------------------------- |
| device_id   | Many2one(device.management.device) |
| date        | Datetime                           |
| user_id     | Many2one(res.users)                |
| title       | Char                               |
| description | Text                               |

Relationship:

* One Device → Many Logs

Pada form device tampilkan tab:

* Maintenance History
* Repair Log

---

## Security & Access Control

Buat security group:

### Device User

Hak akses:

* View device
* View log

Tidak dapat:

* Delete
* Edit data sensitif

---

### Device Manager

Hak akses:

* Create
* Read
* Update
* Delete

Untuk:

* Device
* Device Logs

---

### Device Administrator

Hak akses penuh.

Dapat:

* Mengatur permission
* Mengatur konfigurasi module

---

## One Click Remote Access

Pada form device tampilkan tombol yang menggunakan **Custom URL Protocol** untuk menjalankan remote access langsung dari browser.

### Implementasi

Gunakan Custom URL Protocol handler. Contoh:

#### SSH

```html
<a href="ssh://[user_name]@[ip_address]">Connect SSH</a>
```

Contoh:

```html
<a href="ssh://192.168.1.10">Connect SSH</a>
```

#### RustDesk

```html
<a href="rustdesk://[remote_id]">Connect RustDesk</a>
```

Contoh:

```html
<a href="rustdesk://123456789">Connect RustDesk</a>
```

#### VNC

```html
<a href="vnc://[ip_address]">Connect VNC</a>
```

Contoh:

```html
<a href="vnc://192.168.1.10">Connect VNC</a>
```

### Logika

Jika `remote_type = ssh`, generate URL: `ssh://[user_name]@[ip_address]`
Jika `remote_type = rustdesk`, generate URL: `rustdesk://[remote_id]`
Jika `remote_type = vnc`, generate URL: `vnc://[ip_address]`

### Important Note

Custom URL Protocol memungkinkan browser memanggil aplikasi lokal yang terdaftar sebagai protocol handler di OS user. Pastikan:

1. Aplikasi remote (SSH client, RustDesk, VNC viewer) terdaftar sebagai protocol handler di OS user.
2. Jika protocol handler belum terdaftar, tampilkan command siap copy sebagai fallback.
3. Jangan mengasumsikan browser dapat menjalankan executable lokal tanpa protocol handler yang terdaftar.

---

## User Interface

### Menu Structure

```text
Device Management
├── Devices
├── Maintenance Logs
├── Reports
└── Configuration
```

---

### Device List View

Tampilkan kolom:

* Device Name
* Department
* User
* IP Address
* Operating System
* Device Type
* Usage Type
* Location

---

### Device Form View

Section:

#### General Information

* Device Name
* Department
* User Name
* Location

#### Network

* IP Address
* MAC Address

#### Operating System

* OS
* OS Series
* Serial Number

#### Remote Access

* Remote Type
* Remote ID

#### Notes

* Notes

#### Logs

* Device Logs

---

## Multi Language

Seluruh label harus menggunakan translation mechanism Odoo.

Minimal file:

```text
i18n/
├── en.po
└── id.po
```

Bahasa default:

* English

Bahasa tambahan:

* Indonesian

---

## Technical Requirements

Target Odoo Version:

* Odoo 19

Coding Standard:

* Ikuti Odoo Development Guidelines.
* Gunakan ORM Odoo.
* Hindari raw SQL kecuali benar-benar diperlukan.
* Gunakan access rules dan security groups bawaan Odoo.

---

## Future Enhancements

Persiapkan struktur agar mudah ditambahkan:

* Asset QR Code
* Asset Barcode
* Warranty Tracking
* Software Inventory
* Auto Discovery Agent
* RustDesk API Integration
* Monitoring Agent
* Remote Command Execution
* Device Health Monitoring

---

## Acceptance Criteria

Module dianggap selesai apabila:

1. Device dapat dibuat, diubah, dan dihapus.
2. Device dapat dihubungkan ke department.
3. Device log dapat ditambahkan dari form device.
4. Security group berfungsi sesuai role.
5. Multi-language English dan Indonesian berfungsi.
6. One-click remote menghasilkan command yang sesuai.
7. List view dan form view tersedia.
8. Data dapat diekspor menggunakan fitur Odoo standar.
