# Bài 2: ORM Models & Fields

## Mục lục

1. [Khai báo Model](#1-khai-báo-model)
2. [Các loại Field cơ bản](#2-các-loại-field-cơ-bản)
3. [Multi-company Pattern](#3-multi-company-pattern)
4. [Ví dụ thực tế: `sample.single`](#4-ví-dụ-thực-tế-sample-single)
5. [Truy cập ORM từ code](#5-truy-cập-orm-từ-code)

## 1. Khai báo Model

Mỗi model tương ứng với một bảng trong database. Ví dụ từ `models/category.py`:

```python
from odoo import fields, models, api


class Category(models.Model):
    _name = 'category'
    _description = 'Category'

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")
```

### Các trường đặc biệt (class attributes)

| Trường                  | Mô tả                          | Ví dụ                         |
| ----------------------- | ------------------------------ | ----------------------------- |
| `_name`                 | Tên model (duy nhất hệ thống)  | `'sample.single'`             |
| `_description`          | Mô tả human-readable           | `'Sample Single Description'` |
| `_rec_name`             | Field dùng làm tên hiển thị    | `'name'`                      |
| `_check_company_auto`   | Tự kiểm tra multi-company      | `True`                        |
| `_order`                | Thứ tự mặc định                | `'code, name'`                |

## 2. Các loại Field cơ bản

### Char - Trường văn bản ngắn

```python
code = fields.Char(string='Code', required=True)
name = fields.Char(string='Name')
```

### Text - Trường văn bản dài

```python
description = fields.Text(string='Description')
note = fields.Text(string='Note')
```

### Many2one - Quan hệ 1-N (nhiều records tham chiếu 1 record)

```python
category_id = fields.Many2one('category', string='Category')
company_id = fields.Many2one(
    "res.company", required=True, default=lambda s: s.env.company
)
```

- Field lưu ID của record liên kết trong database
- Thường đặt tên kết thúc bằng `_id`
- `default=lambda s: s.env.company` - giá trị mặc định là company hiện tại

### One2many - Quan hệ 1-N (ngược lại Many2one)

```python
line_ids = fields.One2many(
    'sample.multiple.line',     # Model đích
    'sample_multiple_id',       # Field Many2one trên model đích
    string='Sample Multiple Lines'
)
```

- **Không lưu trong database** - được tính toán từ Many2one bên kia
- Thường đặt tên kết thúc bằng `_ids`

### Các loại Field khác

```python
# Boolean
active = fields.Boolean(string='Active', default=True)

# Integer
quantity = fields.Integer(string='Quantity', default=0)

# Float
price = fields.Float(string='Price', digits=(10, 2))

# Date & DateTime
date = fields.Date(string='Date')
datetime = fields.Datetime(string='Datetime')

# Selection
state = fields.Selection([
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('done', 'Done'),
], string='State', default='draft')

# Binary (file upload)
attachment = fields.Binary(string='Attachment')
```

## 3. Multi-company Pattern

Mọi model nên có `company_id` để hỗ trợ đa công ty:

```python
company_id = fields.Many2one(
    "res.company",
    required=True,
    default=lambda s: s.env.company
)
```

Kết hợp với `_check_company_auto = True` để Odoo tự động kiểm tra quyền company.

## 4. Ví dụ thực tế: `sample.single`

```python
class SampleSingle(models.Model):
    _name = 'sample.single'
    _rec_name = 'name'
    _description = 'Sample Single Description'
    _check_company_auto = True

    # Multi-company
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda s: s.env.company
    )

    # Các field cơ bản
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name')
    category_id = fields.Many2one('category', string='Category')
    description = fields.Text(string='Description')
    note = fields.Text(string='Note')

    # Computed fields (sẽ học ở bài sau)
    compute_field_not_store = fields.Char(
        string='Computed Field Not Stored',
        compute='_compute_field'
    )
    compute_field_store = fields.Char(
        string='Stored Computed Field',
        compute='_compute_field_store',
        store=True
    )
```

## 5. Truy cập ORM từ code

```python
# Tìm kiếm records
records = self.env['sample.single'].search([
    ('name', '=', 'Sample 1'),
    ('company_id', '=', self.env.company.id)
])

# Đếm
count = self.env['sample.single'].search_count([])

# Tạo record
record = self.env['sample.single'].create({
    'code': 'SS-001',
    'name': 'Sample 1',
    'category_id': category.id,
})

# Cập nhật
record.write({'name': 'Updated Name'})

# Xóa
record.unlink()
```
