# Bài 4: Bảo mật - Access Control List (ACL)

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Cấu trúc file ACL](#2-cấu-trúc-file-acl)
3. [Các nhóm quyền mặc định trong Odoo](#3-các-nhóm-quyền-mặc-định-trong-odoo)
4. [Ví dụ thực tế](#4-ví-dụ-thực-tế)
5. [Quy tắc quan trọng](#5-quy-tắc-quan-trọng)
6. [Quyền nâng cao - Record Rules](#6-quyền-nâng-cao---record-rules)

## 1. Tổng quan

Odoo sử dụng hệ thống ACL để kiểm soát quyền truy cập model. ACL được định nghĩa trong file CSV:

```text
security/ir.model.access.csv
```

## 2. Cấu trúc file ACL

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_ps_category,access_ps_category,model_category,base.group_user,1,0,0,0
access_ps_category_admin,access_ps_category_admin,model_category,base.group_system,1,1,1,1
```

### Giải thích từng cột

| Cột             | Mô tả                       | Ví dụ                              |
| --------------- | --------------------------- | ---------------------------------- |
| `id`            | XML ID duy nhất             | `access_ps_category`               |
| `name`          | Tên rule                    | `access_ps_category`               |
| `model_id:id`   | Model cần cấp quyền         | `model_category`                   |
| `group_id:id`   | Nhóm user được cấp          | `base.group_user`                  |
| `perm_read`     | Quyền đọc                   | `1` (có) / `0` (không)             |
| `perm_write`    | Quyền ghi                   | `1` / `0`                          |
| `perm_create`   | Quyền tạo                   | `1` / `0`                          |
| `perm_unlink`   | Quyền xóa                   | `1` / `0`                          |

### Quy tắc đặt tên `model_id:id`

Thay `.` bằng `_` và thêm `model_` ở đầu:

- `sample.single` -> `model_sample_single`
- `category` -> `model_category`
- `sample.multiple.line` -> `model_sample_multiple_line`

## 3. Các nhóm quyền mặc định trong Odoo

| Nhóm                    | Mô tả                          |
| ----------------------- | ------------------------------ |
| `base.group_user`       | User thông thường (đã xác thực) |
| `base.group_system`     | Administrator (Settings)       |
| `base.group_public`     | Guest (chưa đăng nhập)         |
| `base.group_portal`     | Portal user                    |

## 4. Ví dụ thực tế

File `security/ir.model.access.csv` từ module mẫu:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_ps_category,access_ps_category,model_category,base.group_user,1,0,0,0
access_ps_category_admin,access_ps_category_admin,model_category,base.group_system,1,1,1,1
access_ps_sample_single,access_ps_sample_single,model_sample_single,base.group_user,1,0,0,0
access_ps_sample_single_admin,access_ps_sample_single_admin,model_sample_single,base.group_system,1,1,1,1
access_ps_sample_multiple,access_ps_sample_multiple,model_sample_multiple,base.group_user,1,0,0,0
access_ps_sample_multiple_admin,access_ps_sample_multiple_admin,model_sample_multiple,base.group_system,1,1,1,1
access_ps_sample_multiple_line,access_ps_sample_multiple_line,model_sample_multiple_line,base.group_user,1,0,0,0
access_ps_sample_multiple_line_admin,access_ps_sample_multiple_line_admin,model_sample_multiple_line,base.group_system,1,1,1,1
```

### Phân tích

| Model                  | User thông thường | Admin      |
| ---------------------- | ----------------- | ---------- |
| `category`             | Read only         | Full CRUD  |
| `sample.single`        | Read only         | Full CRUD  |
| `sample.multiple`      | Read only         | Full CRUD  |
| `sample.multiple.line` | Read only         | Full CRUD  |

**Mô hình**: User thường chỉ được xem, admin được quản lý tất cả.

## 5. Quy tắc quan trọng

### ACL phải load trước Views

Trong `__manifest__.py`:

```python
'data': [
    'security/ir.model.access.csv',  # ← Đầu tiên!
    'views/category_views.xml',
    'views/sample_single.xml',
    'views/sample_multiple.xml',
    'views/menus.xml'
]
```

Nếu ACL load sau views, Odoo sẽ lỗi khi render view.

### Mỗi model cần ít nhất 1 ACL rule

Nếu model không có ACL, user sẽ không thể truy cập model đó.

### Test ACL

1. Đăng nhập với user thường (không phải admin)
2. Thử tạo/sửa/xóa records
3. Nếu bị từ chối, kiểm tra ACL

## 6. Quyền nâng cao - Record Rules

ACL kiểm soát quyền trên **model level**. Record Rules kiểm soát trên **record level**:

```python
# Ví dụ: User chỉ thấy records của company mình
rule = self.env['ir.rule'].create({
    'name': 'Company Rule',
    'model_id': self.env['ir.model']._get_id('sample.single'),
    'domain_force': "[('company_id', 'in', [False] + user.company_ids.ids)]",
    'groups': [(4, self.env.ref('base.group_user').id)],
})
```
