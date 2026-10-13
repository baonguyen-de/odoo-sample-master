# Bài 0: Tổng quan Odoo 19 & Cài đặt môi trường

## Mục lục

1. [Odoo là gì?](#1-odoo-là-gì)
2. [Source code mẫu & Hướng dẫn Clone](#2-source-code-mẫu--hướng-dẫn-clone)
3. [Kiến trúc tổng quan](#3-kiến-trúc-tổng-quan)
4. [Cấu trúc thư mục dự án](#4-cấu-trúc-thư-mục-dự-án)
5. [Cài đặt với Docker](#5-cài-đặt-với-docker)
6. [Cấu hình Custom Addons](#6-cấu-hình-custom-addons)

## 1. Odoo là gì?

Odoo là một bộ ứng dụng quản lý doanh nghiệp mã nguồn mở (open-source ERP), bao gồm:

- **CRM** - Quản lý quan hệ khách hàng
- **Sales** - Bán hàng
- **Inventory** - Quản lý kho
- **Accounting** - Kế toán
- **Manufacturing** - Sản xuất
- **HR** - Nhân sự
- ... và hàng trăm module khác

Odoo 19 là phiên bản mới nhất, sử dụng Python (backend) và JavaScript/XML (frontend).

## 2. Source code mẫu & Hướng dẫn Clone

Toàn bộ source code minh họa trong seminar được lưu tại GitHub:

- **Repository:** <https://github.com/patsoft-dev/odoo-sample>

### Clone về máy

```bash
git clone https://github.com/patsoft-dev/odoo-sample.git
cd odoo-sample
```

### Cập nhật code mới nhất

```bash
git pull origin master
```

### Xem các branch/tag

```bash
git branch -a
git tag
```

## 3. Kiến trúc tổng quan

```text
┌─────────────────────────────────────┐
│           Web Browser               │
│         (JavaScript/XML)            │
├─────────────────────────────────────┤
│         Odoo Server (Python)        │
│  ┌───────────┐  ┌───────────────┐   │
│  │   ORM     │  │  Controller   │   │
│  │ (Models)  │  │   (Routes)    │   │
│  └─────┬─────┘  └───────────────┘   │
├────────┼────────────────────────────┤
│        │     PostgreSQL Database     │
│        └────────────────────────────┘
```

## 4. Cấu trúc thư mục dự án

```text
sample/
├── docker-compose.yml          # Docker setup (Odoo 19 + PostgreSQL)
├── custom_addons/              # Thư mục chứa custom modules
│   └── ps_accounting_sample/   # Module mẫu
│       ├── __manifest__.py     # Metadata của module
│       ├── __init__.py         # Import packages
│       ├── models/             # ORM Models (Python)
│       ├── views/              # Giao diện (XML)
│       ├── security/           # Quyền truy cập (ACL)
│       └── demo/               # Dữ liệu mẫu
├── odoo_backup_guide.md        # Hướng dẫn backup (CLI)
└── odoo_web_backup_guide.md    # Hướng dẫn backup (Web)
```

## 5. Cài đặt với Docker

### Yêu cầu

- Docker & Docker Compose đã cài đặt

### Khởi động

```bash
docker compose up -d
```

### Truy cập

- **Odoo**: <http://localhost:8869>
- **PostgreSQL**: `localhost:5443`

### Thông tin đăng nhập PostgreSQL

| Thông tin | Giá trị     |
| --------- | ----------- |
| Host      | `db`        |
| Port      | `5432`      |
| User      | `odoo`      |
| Password  | `odooodoo`  |

### Tạo database mới

1. Truy cập <http://localhost:8869>
2. Nhấn **Create Database**
3. Nhập tên database, email, password
4. **Tick "Load demonstration data"** để có dữ liệu mẫu
5. Nhấn **Create**

## 6. Cấu hình Custom Addons

Trong `docker-compose.yml`, thư mục `custom_addons` được mount vào Odoo:

```yaml
volumes:
  - ./custom_addons:/mnt/extra-addons
```

Odoo sẽ tự động quét thư mục `/mnt/extra-addons` để tìm các custom modules.
