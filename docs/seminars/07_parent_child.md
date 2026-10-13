# Bài 7: Quan hệ Parent-Child (One2many / Many2one)

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Ví dụ từ dự án](#2-ví-dụ-từ-dự-án)
3. [ondelete Options](#3-ondelete-options)
4. [View cho Parent-Child](#4-view-cho-parent-child)
5. [Truy cập dữ liệu Parent-Child](#5-truy-cập-dữ-liệu-parent-child)
6. [Xóa Parent có Child](#6-xóa-parent-có-child)
7. [Demo Data cho Parent-Child](#7-demo-data-cho-parent-child)
8. [Action Method cho Parent](#8-action-method-cho-parent)

## 1. Tổng quan

Quan hệ Parent-Child là pattern phổ biến nhất trong Odoo:

- **Parent**: Model chứa nhiều child records (One2many)
- **Child**: Model tham chiếu parent (Many2one)

Ví dụ: Đơn hàng (Parent) - Dòng đơn hàng (Child)

## 2. Ví dụ từ dự án

### Parent Model: `sample.multiple`

```python
class SampleMultiple(models.Model):
    _name = 'sample.multiple'
    _rec_name = 'name'

    company_id = fields.Many2one("res.company", required=True, default=lambda s: s.env.company)
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    category_id = fields.Many2one('category', string='Category')
    description = fields.Text(string='Description')
    note = fields.Text(string='Note')

    # One2many: Liên kết với child records
    line_ids = fields.One2many(
        'sample.multiple.line',      # Model child
        'sample_multiple_id',        # Field Many2one trên child
        string='Sample Multiple Lines'
    )
```

### Child Model: `sample.multiple.line`

```python
class SampleMultipleLine(models.Model):
    _name = 'sample.multiple.line'
    _rec_name = 'name'

    company_id = fields.Many2one("res.company", required=True, default=lambda s: s.env.company)

    # Many2one: Liên kết với parent
    sample_multiple_id = fields.Many2one(
        'sample.multiple',
        string='Sample Multiple',
        ondelete='cascade'      # Xóa child khi parent bị xóa
    )

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
```

## 3. ondelete Options

| Option        | Hành vi khi parent bị xóa                       |
| ------------- | ----------------------------------------------- |
| `cascade`     | Xóa luôn child records                          |
| `set null`    | Đặt field Many2one = NULL (mặc định)            |
| `restrict`    | Không cho xóa parent nếu có child               |

```python
# Cascade: Xóa child khi parent bị xóa
sample_multiple_id = fields.Many2one('sample.multiple', ondelete='cascade')

# Set null: Để field trống khi parent bị xóa
sample_multiple_id = fields.Many2one('sample.multiple', ondelete='set null')

# Restrict: Không cho xóa parent
sample_multiple_id = fields.Many2one('sample.multiple', ondelete='restrict')
```

## 4. View cho Parent-Child

### Form View với Inline Editable List

```xml
<form string="Sample multiple">
    <sheet>
        <!-- Các field của parent -->
        <group>
            <field name="name"/>
            <field name="category_id"/>
        </group>

        <!-- Tab chứa child records -->
        <notebook>
            <page name="lines" string="Lines">
                <field name="line_ids">
                    <list editable="bottom">
                        <field name="code"/>
                        <field name="name"/>
                        <field name="description"/>
                    </list>
                </field>
            </page>
        </notebook>
    </sheet>
</form>
```

### Kết quả giao diện

```text
┌──────────────────────────────────────────┐
│  Sample Multiple 1                       │
│  Category: Office Supplies               │
├──────────────────────────────────────────┤
│  [Lines]                                 │
│  ┌───────┬───────────────┬────────────┐  │
│  │ Code  │ Name          │ Desc       │  │
│  ├───────┼───────────────┼────────────┤  │
│  │ SM-01 │ Line A        │ ...        │  │
│  │ SM-02 │ Line B        │ ...        │  │
│  │       │ + Thêm dòng mới              │  │
│  └───────┴───────────────┴────────────┘  │
└──────────────────────────────────────────┘
```

## 5. Truy cập dữ liệu Parent-Child

### Từ Parent đến Child

```python
parent = self.env['sample.multiple'].browse(1)

# Lấy tất cả child records
children = parent.line_ids

# Đếm child records
count = len(parent.line_ids)

# Tìm child theo điều kiện
filtered = parent.line_ids.filtered(lambda r: r.code == 'SM-001')
```

### Từ Child đến Parent

```python
child = self.env['sample.multiple.line'].browse(1)

# Lấy parent record
parent = child.sample_multiple_id

# Lấy parent name
parent_name = child.sample_multiple_id.name
```

### Tìm kiếm liên quan

```python
# Tìm tất cả child records của parent có code = 'SM-001'
children = self.env['sample.multiple.line'].search([
    ('sample_multiple_id.code', '=', 'SM-001')
])

# Tìm parents có child records
parents = self.env['sample.multiple'].search([
    ('line_ids', '!=', False)
])
```

## 6. Xóa Parent có Child

### Với ondelete='cascade'

```python
# Tự động xóa tất cả child records
parent.unlink()  # -> Cả parent và children đều bị xóa
```

### Validate trước khi xóa

```python
def unlink(self):
    # Không cho xóa nếu còn child records
    if len(self.line_ids):
        raise UserError(_("Cannot delete record because it has related lines."))
    return super().unlink()
```

## 7. Demo Data cho Parent-Child

### Parent Records

```xml
<record id="sample_multiple_1" model="sample.multiple">
    <field name="company_id" ref="base.main_company" />
    <field name="code">SM-001</field>
    <field name="name">Sample Multiple 1</field>
    <field name="category_id" ref="ps_accounting_sample.category_1" />
</record>
```

### Child Records (tham chiếu parent qua XML ID)

```xml
<record id="sample_multiple_line_1" model="sample.multiple.line">
    <field name="company_id" ref="base.main_company" />
    <field name="sample_multiple_id" ref="ps_accounting_sample.sample_multiple_1" />
    <field name="code">SML-001</field>
    <field name="name">Line A</field>
</record>
```

- `ref="ps_accounting_sample.sample_multiple_1"` - Tham chiếu parent record qua XML ID

## 8. Action Method cho Parent

```python
def action_line_count(self):
    """Đếm số dòng child và cập nhật vào note"""
    self.ensure_one()
    line_count = self.env['sample.multiple.line'].search_count([
        ('sample_multiple_id', '=', self.id)
    ])
    self.note = f"This sample has {line_count} related lines."

    return {
        "type": "ir.actions.client",
        'tag': 'display_notification',
        "params": {
            "message": "Line count has been updated.",
            "type": "success",
            "next": {
                "type": "ir.actions.client",
                "tag": "soft_reload",
            }
        },
    }
```
