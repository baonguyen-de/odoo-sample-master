# Bài 1: Cấu trúc Module Odoo

## Mục lục

1. [Cấu trúc thư mục](#1-cấu-trúc-thư-mục)
2. [`__manifest__.py`](#2-__manifest__py)
3. [Import Chain](#3-import-chain)
   - 3.1. [Root `__init__.py`](#31-root-__init__py)
   - 3.2. [`__init__.py` của từng package con](#32-__init__py-của-từng-package-con)
   - 3.3. [Quy tắc](#33-quy-tắc)
4. [Quy tắc đặt tên](#4-quy-tắc-đặt-tên)

Mỗi module Odoo là một Python package với cấu trúc thư mục chuẩn.

## 1. Cấu trúc thư mục

```text
ps_accounting_sample/
├── __manifest__.py         # Metadata của module
├── __init__.py             # Import sub-packages
├── models/
│   ├── __init__.py         # Import từng model
│   ├── category.py
│   ├── sample_single.py
│   ├── sample_multiple.py
│   └── sample_multiple_line.py
├── views/
│   ├── category_views.xml  # Views + Actions
│   ├── sample_single.xml
│   ├── sample_multiple.xml
│   └── menus.xml           # Cấu trúc menu
├── security/
│   └── ir.model.access.csv # Quyền truy cập (ACL)
└── demo/
    ├── category.csv
    ├── sample_single.xml
    ├── sample_multiple.xml
    └── sample_multiple_line.xml
```

## 2. `__manifest__.py`

Đây là file quan trọng nhất, khai báo mọi thông tin về module.

**Ví dụ:**

```python
{
    'name': 'PS Accounting Sample',
    'description': 'PatSoft Accounting Sample module',
    'category': 'PatSoft/Accounting Sample',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/category_views.xml',
        'views/sample_single.xml',
        'views/sample_multiple.xml',
        'views/menus.xml',
    ],
    'demo': [
        'demo/category.csv',
        'demo/sample_multiple.xml',
        'demo/sample_multiple_line.xml',
        'demo/sample_single.xml',
    ],
    'application': True,
}
```

**Các trường quan trọng:**

| Trường        | Mô tả                                                         |
| ------------- | ------------------------------------------------------------- |
| `name`        | Tên hiển thị của module                                        |
| `description` | Mô tả ngắn                                                    |
| `category`    | Phân loại module                                               |
| `depends`     | Danh sách modules phụ thuộc                                    |
| `data`        | File data load khi cài (**thứ tự quan trọng!**)               |
| `demo`        | File demo data (chỉ load khi tick "Load demonstration data")  |
| `application` | `True` nếu module là app độc lập                              |

**Thứ tự load trong `data`:**

> **Rất quan trọng!** Odoo load file theo thứ tự trong danh sách `data`:
>
> 1. **Security** (`ir.model.access.csv`) phải load **trước** views
> 2. **Views** load trước **menus** (vì menus tham chiếu actions)

## 3. Import Chain

`__init__.py` chỉ chứa các lệnh import, không chứa logic. Mỗi package con (sub-folder) trong module phải được import ở `__init__.py` tương ứng cấp.

### 3.1. Root `__init__.py`

Import tất cả package con của module. Nếu module có thêm `controllers/`, `wizards/`, `reports/`... thì phải import tương ứng:

```python
from . import models
from . import controllers
from . import wizards
from . import reports
```

> Module nào chỉ có `models/` thì chỉ cần `from . import models`.

### 3.2. `__init__.py` của từng package con

Mỗi package con (ví dụ `models/`, `controllers/`, `wizards/`) có file `__init__.py` riêng, dùng để import các file Python bên trong nó.

**`models/__init__.py`:**

```python
from . import category
from . import sample_single
from . import sample_multiple
from . import sample_multiple_line
```

**`controllers/__init__.py`:**

```python
from . import main
```

**`wizards/__init__.py`:**

```python
from . import sample_wizard
```

### 3.3. Quy tắc

> Mỗi file Python (model, controller, wizard...) phải được import trong `__init__.py` của package chứa nó, nếu không Odoo sẽ không nhận diện được.

## 4. Quy tắc đặt tên

| Loại           | Quy tắc                  | Ví dụ                          |
| -------------- | ------------------------ | ------------------------------ |
| Module         | `snake_case`             | `ps_accounting_sample`         |
| Model          | `dot.notation`           | `sample.single`                |
| Python class   | `CamelCase`              | `SampleSingle`                 |
| Field          | `snake_case`             | `category_id`, `line_ids`      |
| View XML ID    | `module_action_model`    | `sample_single_view_form`      |

### Đặt tên model

- Dùng `dot.notation`: `sample.single`, `sample.multiple.line`
- Tên phải **duy nhất** trong toàn hệ thống
- Odoo tự chuyển `.` thành `_` trong database: `sample_single`

### Đặt tên field

- Field Many2one thường kết thúc bằng `_id`: `category_id`
- Field One2many thường kết thúc bằng `_ids`: `line_ids`
- Field Many2many thường kết thúc bằng `_ids`: `tag_ids`
