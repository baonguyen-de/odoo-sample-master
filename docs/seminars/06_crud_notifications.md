# Bài 6: CRUD Overrides & Thông báo

## Mục lục

1. [Tổng quan CRUD](#1-tổng-quan-crud)
2. [Create - Tạo record](#2-create---tạo-record)
3. [Write - Cập nhật record](#3-write---cập-nhật-record)
4. [Unlink - Xóa record](#4-unlink---xóa-record)
5. [Thông báo Bus Notification](#5-thông-báo-bus-notification)
6. [Action Methods](#6-action-methods)
7. [Logger](#7-logger)

## 1. Tổng quan CRUD

Odoo cho phép override 3 method CRUD chính:

- `create` - Tạo record mới
- `write` - Cập nhật record
- `unlink` - Xóa record

## 2. Create - Tạo record

```python
@api.model_create_multi
def create(self, vals_list):
    # vals_list là list các dict, mỗi dict = 1 record mới

    for val in vals_list:
        if 'name' not in val or not val['name']:
            raise UserError(_("Sample name is required."))

    return super(SampleSingle, self).create(vals_list)
```

### Giải thích

| Thành phần                 | Mô tả                                          |
| -------------------------- | ---------------------------------------------- |
| `@api.model_create_multi`  | Decorator cho create method (Odoo 17+)         |
| `vals_list`                | Danh sách dict `[{'name': 'A'}, {'name': 'B'}]` |
| `super()`                  | Gọi method create của lớp cha                  |

### So sánh với cách cũ

```python
# Cũ (Odoo 16 và trước)
@api.model
def create(self, vals):
    # vals là 1 dict
    return super().create(vals)

# Mới (Odoo 17+)
@api.model_create_multi
def create(self, vals_list):
    # vals_list là list dict
    return super().create(vals_list)
```

## 3. Write - Cập nhật record

```python
def write(self, vals):
    # vals là dict chứa các field cần cập nhật

    # Validate trước khi update
    if 'name' in vals and not vals.get('name'):
        raise UserError(_("Sample name is required."))

    # Tự động cập nhật field khác
    vals['note'] = f"Record updated with name: {vals.get('name', 'No Name')}"

    # Gọi method cha
    result = super(SampleSingle, self).write(vals)

    # Gửi thông báo sau khi update thành công
    if result:
        self.env.user._bus_send(
            "simple_notification",
            {
                "title": _("Record Updated"),
                "type": "success",
                "message": "The record has been updated successfully.",
                "sticky": False,
            }
        )
    return result
```

### vals dictionary

```python
# Khi user sửa field 'name' và 'description':
vals = {
    'name': 'New Name',
    'description': 'New Description'
}

# Khi dùng code:
record.write({'name': 'New Name'})
```

## 4. Unlink - Xóa record

```python
def unlink(self):
    # Validate trước khi xóa
    if self.search_count([]) == len(self):
        raise UserError(_("Cannot delete all records."))

    # Gọi method cha
    return super(SampleSingle, self).unlink()
```

### Ví dụ thực tế: Kiểm tra trước khi xóa

```python
# Không cho xóa record có child lines
def unlink(self):
    if len(self.line_ids):
        raise UserError(_("Cannot delete record because it has related lines."))
    return super().unlink()
```

## 5. Thông báo Bus Notification

### Gửi thông báo từ code

```python
self.env.user._bus_send(
    "simple_notification",
    {
        "title": _("Record Updated"),           # Tiêu đề
        "type": "success",                       # info | warning | danger | success
        "message": "The record has been updated successfully.",  # Nội dung
        "sticky": False,                         # True = dính màn hình, False = tự biến mất
    }
)
```

### Các loại thông báo

| type       | Màu sắc     | Dùng khi              |
| ---------- | ----------- | --------------------- |
| `info`     | Xanh dương  | Thông tin chung       |
| `success`  | Xanh lá     | Thao tác thành công   |
| `warning`  | Vàng        | Cảnh báo              |
| `danger`   | Đỏ          | Lỗi nghiêm trọng     |

### Trả về action notification từ method

```python
def action_reset_description(self):
    self.ensure_one()
    self.description = "Default description"

    return {
        "type": "ir.actions.client",
        'tag': 'display_notification',
        "params": {
            "message": "Description has been reset to default.",
            "type": "success",
            "next": {
                "type": "ir.actions.client",
                "tag": "soft_reload",  # Reload view mà không refresh trang
            }
        },
    }
```

### Giải thích

| Thành phần                       | Mô tả                                                |
| -------------------------------- | ---------------------------------------------------- |
| `type: "ir.actions.client"`      | Action type cho client                               |
| `tag: 'display_notification'`    | Hiển thị toast notification                          |
| `next.tag: "soft_reload"`        | Sau khi đóng notification, reload view               |

## 6. Action Methods

Method được gọi từ button trên form view:

```python
# Python
def action_line_count(self):
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

```xml
<!-- XML -->
<button name="action_line_count"
        string="Line Count"
        type="object"
        class="btn-info" />
```

### `ensure_one()`

Đảm bảo method chỉ chạy trên 1 record:

```python
def action_something(self):
    self.ensure_one()  # Nếu self chứa nhiều records -> raise error
    # Code xử lý 1 record
```

## 7. Logger

```python
import logging
_logger = logging.getLogger(__name__)

# Sử dụng
_logger.info("Record updated: %s", record.id)
_logger.warning("Something might be wrong: %s", data)
_logger.error("Error occurred: %s", error)
```
