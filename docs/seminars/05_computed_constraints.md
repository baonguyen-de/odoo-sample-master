# Bài 5: Computed Fields & Constraints

## Mục lục

1. [Computed Fields - Trường được tính toán](#1-computed-fields---trường-được-tính-toán)
2. [`@api.depends`](#2-apidepends)
3. [`_compute_display_name`](#3-_compute_display_name)
4. [SQL Constraints](#4-sql-constraints)
5. [Python Constraints](#5-python-constraints)
6. [`@api.onchange`](#6-apionchange)

## 1. Computed Fields - Trường được tính toán

Computed fields tự động tính giá trị dựa trên các field khác.

### Không lưu trong DB (store=False)

```python
compute_field_not_store = fields.Char(
    string='Computed Field Not Stored',
    compute='_compute_field'
)

@api.depends('name', 'category_id')
def _compute_field(self):
    for rec in self:
        rec.compute_field_not_store = f"{rec.name} - {rec.category_id.name if rec.category_id else 'No Category'}"
```

- Giá trị được tính **mỗi lần đọc**
- **Không lưu** trong database
- Không thể search/filter theo field này

### Lưu trong DB (store=True)

```python
compute_field_store = fields.Char(
    string='Stored Computed Field',
    compute='_compute_field_store',
    store=True
)

@api.depends('name', 'category_id')
def _compute_field_store(self):
    for rec in self:
        rec.compute_field_store = f"{rec.name} - {rec.category_id.name if rec.category_id else 'No Category'}"
```

- Giá trị được tính khi **dependencies thay đổi**
- **Lưu** trong database
- Có thể search/filter theo field này

### So sánh

| Tính năng       | store=False | store=True               |
| --------------- | ----------- | ------------------------ |
| Lưu trong DB    | Không       | Có                       |
| Khi nào tính    | Mỗi lần đọc | Khi dependencies thay đổi |
| Search được     | Không       | Có                       |
| Hiệu suất       | Chậm khi nhiều reads | Nhanh khi đọc  |

## 2. `@api.depends`

`@api.depends` khai báo các field mà computed field phụ thuộc vào:

```python
@api.depends('name', 'category_id')
def _compute_field(self):
    ...
```

- Khi `name` hoặc `category_id` thay đổi -> computed field được tính lại
- Nếu dùng `store=True`, giá trị mới sẽ được lưu vào DB

### Phụ thuộc nested

```python
@api.depends('category_id.name')
def _compute_field(self):
    for rec in self:
        rec.computed = rec.category_id.name or ''
```

## 3. `_compute_display_name`

Override phương thức này để tùy chỉnh tên hiển thị của record:

```python
@api.depends("code", "name")
def _compute_display_name(self):
    for rec in self:
        if self.env.context.get('show_code_only', False):
            rec.display_name = rec.code
        else:
            if rec.code and rec.name:
                rec.display_name = f'[{rec.code}] {rec.name}'
            else:
                rec.display_name = ""
```

- `display_name` được hiển thị trong Many2one dropdown
- Có thể dùng `context` để thay đổi cách hiển thị

## 4. SQL Constraints

Ràng buộc ở cấp database, hiệu suất cao nhất:

```python
_sample_single_code_unique = models.Constraint(
    'unique(company_id, code)',
    _('Sample Single Code must be unique.')
)
```

### Các loại SQL Constraint phổ biến

```python
# Unique: Mỗi company chỉ có 1 code duy nhất
_sample_single_code_unique = models.Constraint(
    'unique(company_id, code)',
    _('Code must be unique per company.')
)

# Check: Giá trị phải > 0
_positive_quantity = models.Constraint(
    'CHECK(quantity > 0)',
    _('Quantity must be positive.')
)

# Foreign key (thường ORM tự xử lý)
```

### Syntax mới (Odoo 17+)

Odoo 17+ dùng `models.Constraint()` thay cho `_sql_constraints` cũ:

```python
# Cũ (Odoo 16 và trước)
_sql_constraints = [
    ('code_uniq', 'unique(company_id, code)', 'Code must be unique.')
]

# Mới (Odoo 17+)
_sample_single_code_unique = models.Constraint(
    'unique(company_id, code)',
    _('Code must be unique.')
)
```

## 5. Python Constraints

Ràng buộc bằng Python code, linh hoạt hơn SQL:

```python
@api.constrains("code")
def _check_code(self):
    for rec in self:
        if not rec.code:
            raise UserError(_("Item Code is required."))
```

### Ví dụ phức tạp hơn

```python
@api.constrains('date_start', 'date_end')
def _check_dates(self):
    for rec in self:
        if rec.date_start and rec.date_end:
            if rec.date_start > rec.date_end:
                raise UserError(_("Start date must be before end date."))
```

### So sánh SQL vs Python Constraints

| Tính năng          | SQL Constraint  | Python Constraint |
| ------------------ | --------------- | ----------------- |
| Hiệu suất          | Cao (DB level)  | Thấp hơn          |
| Linh hoạt          | Hạn chế         | Tùy ý             |
| Kiểm tra phức tạp  | Khó             | Dễ                |
| Thông báo lỗi      | Tùy DB          | Tùy ý             |

## 6. `@api.onchange`

Tự động thay đổi giá trị field khi field khác thay đổi trên form:

```python
@api.onchange("category_id")
def _onchange_category_id(self):
    if self.category_id:
        self.description = f"Selected category: {self.category_id.name}"
    else:
        self.description = "No category selected"
```

- **Chỉ hoạt động trên form view** (không hoạt động khi dùng code)
- Thay đổi **chưa lưu** cho đến khi user nhấn Save

### So sánh onchange vs compute

| Tính năng            | `@api.onchange`              | `@api.depends` (compute)   |
| -------------------- | ---------------------------- | -------------------------- |
| Khi nào chạy         | User thay đổi field          | Data thay đổi (bất kỳ đâu) |
| Lưu trong DB         | Không (chỉ trên form)        | Có thể (nếu `store=True`)  |
| Hoạt động trong code | Không                        | Có                         |
