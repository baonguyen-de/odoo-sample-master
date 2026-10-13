# Bài 3: Views (XML) - Giao diện Odoo

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [List View (Bảng)](#2-list-view-bảng)
3. [Form View (Chi tiết)](#3-form-view-chi-tiết)
4. [Search View (Tìm kiếm)](#4-search-view-tìm-kiếm)
5. [Window Action - Liên kết Model với View](#5-window-action---liên-kết-model-với-view)
6. [Menus](#6-menus)
7. [Button trong Form](#7-button-trong-form)

## 1. Tổng quan

Mỗi model thường có 3 loại view chính:

- **List** (trước đây gọi là `tree`) - Hiển thị dạng bảng
- **Form** - Chi tiết một record
- **Search** - Bộ lọc tìm kiếm

## 2. List View (Bảng)

```xml
<record id="sample_single_view_list" model="ir.ui.view">
    <field name="name">Sample Single</field>
    <field name="model">sample.single</field>
    <field name="arch" type="xml">
        <list string="">
            <field name="code" />
            <field name="name" />
            <field name="category_id" />
            <field name="description"/>
            <field name="note" />
        </list>
    </field>
</record>
```

**Lưu ý**: Odoo 17+ dùng `<list>` thay vì `<tree>` cũ.

### List Inline Editable

Dùng cho model có quan hệ parent-child (One2many):

```xml
<field name="line_ids">
    <list editable="bottom">
        <field name="code"/>
        <field name="name"/>
        <field name="description"/>
    </list>
</field>
```

- `editable="bottom"` - Thêm dòng mới ở cuối bảng
- `editable="top"` - Thêm dòng mới ở đầu bảng

## 3. Form View (Chi tiết)

```xml
<record id="sample_single_view_form" model="ir.ui.view">
    <field name="name">Sample Single</field>
    <field name="model">sample.single</field>
    <field name="arch" type="xml">
        <form string="Sample Single">
            <!-- Phần header: Buttons & Status bar -->
            <header>
                <button name="action_reset_description"
                        string="Reset Description"
                        type="object"
                        class="btn-info" />
            </header>

            <!-- Phần sheet: Nội dung chính -->
            <sheet name="item-form">
                <!-- Field ẩn -->
                <field name="company_id" invisible="1" />

                <!-- Title block -->
                <div class="oe_title">
                    <label for="code" string="Code" />
                    <h1>
                        <div class="d-flex">
                            <field class="text-break" name="code"
                                   options="{'line_breaks': False}" widget="text" />
                        </div>
                    </h1>
                </div>

                <!-- Nhóm field 2 cột -->
                <group name="first">
                    <group>
                        <field name="name"/>
                    </group>
                    <group>
                        <field name="category_id"/>
                    </group>
                </group>

                <!-- Tab notebook -->
                <notebook>
                    <page name="general" string="General">
                        <group name="second">
                            <group string="Info 1">
                                <field name="description"/>
                            </group>
                            <group string="Info 2">
                                <field name="note"/>
                            </group>
                        </group>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

### Cấu trúc Form view

```text
<form>
├── <header>                       # Buttons, status bar
└── <sheet>                        # Nội dung chính
    ├── Field ẩn                   # invisible="1"
    ├── <div class="oe_title">     # Title block
    ├── <group>                    # Nhóm field (2 cột)
    └── <notebook>                 # Các tab
        └── <page>                 # Một tab
```

### Các thuộc tính quan trọng

| Thuộc tính       | Mô tả                          |
| ---------------- | ------------------------------ |
| `invisible="1"`  | Ẩn field (vẫn lưu trong DB)    |
| `required="1"`   | Bắt buộc nhập                  |
| `readonly="1"`   | Chỉ đọc                        |
| `string="..."`   | Label hiển thị                 |

## 4. Search View (Tìm kiếm)

```xml
<record id="search_document_view" model="ir.ui.view">
    <field name="name">search_document_view</field>
    <field name="model">category</field>
    <field name="arch" type="xml">
        <search string="Document">
            <field name="name"/>
            <field name="code"/>
        </search>
    </field>
</record>
```

### Bộ lọc có sẵn

```xml
<search>
    <field name="name"/>
    <!-- Bộ lọc theo group -->
    <group expand="0" string="Group By">
        <filter name="group_by_category"
                string="Category"
                domain="[]"
                context="{'group_by': 'category_id'}" />
    </group>
</search>
```

## 5. Window Action - Liên kết Model với View

```xml
<record id="action_sample_single_view" model="ir.actions.act_window">
    <field name="name">Sample Single</field>
    <field name="res_model">sample.single</field>
    <field name="view_mode">list,form</field>
</record>
```

| Trường        | Mô tả                                       |
| ------------- | ------------------------------------------- |
| `res_model`   | Model cần hiển thị                          |
| `view_mode`   | Các view type (phân cách bằng dấu phẩy)     |

**Odoo 17+**: Dùng `list,form` thay vì `tree,form`

## 6. Menus

```xml
<!-- Menu gốc -->
<menuitem id="root_menu" name="Sample" sequence="0"/>

<!-- Sub menu con -->
<menuitem id="sample_single_sub_menu"
          name="Sample Single"
          parent="root_menu"
          sequence="10"
          action="action_sample_single_view"/>

<!-- Menu nhóm (không có action) -->
<menuitem id="config_sub_menu"
          name="Config"
          parent="root_menu"
          sequence="100"/>

<!-- Menu con của nhóm -->
<menuitem id="category_sub_menu"
          name="Category"
          parent="config_sub_menu"
          sequence="10"
          action="action_category_view"/>
```

### Cấu trúc menu

```text
Sample (root_menu)
├── Sample Single (action: action_sample_single_view)
├── Sample Multiple (action: action_sample_multiple_view)
└── Config (config_sub_menu)
    └── Category (action: action_category_view)
```

- `parent` - Menu cha
- `sequence` - Thứ tự hiển thị (số nhỏ hơn nằm trên)
- `action` - Action được gọi khi click menu

## 7. Button trong Form

```xml
<!-- Button gọi Python method -->
<button name="action_reset_description"
        string="Reset Description"
        type="object"
        class="btn-info" />
```

| Thuộc tính         | Mô tả                                          |
| ------------------ | ---------------------------------------------- |
| `name`             | Tên method Python                              |
| `type="object"`    | Gọi method trên model                          |
| `string`           | Label hiển thị                                 |
| `class`            | CSS class (btn-info, btn-primary, btn-danger)  |
