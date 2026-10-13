from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class SampleSingle(models.Model):
    # 1. Các trường đặc biệt của model:
    # Trường _name xác định tên của mô hình, được sử dụng để tham chiếu đến mô hình trong Odoo. Tên này phải là duy nhất trong hệ thống.
    _name = 'sample.single'
    # Trường _rec_name xác định trường nào sẽ được sử dụng làm tên hiển thị cho bản ghi. Nếu không được chỉ định, Odoo sẽ sử dụng trường 'name' mặc định.
    _rec_name = 'name'
    # Trường _description mô tả về model.
    _description = 'Sample Single Description'
    # Trường _check_company_auto nếu được đặt thành True, Odoo sẽ tự động kiểm tra rằng tất cả các bản ghi của mô hình này đều thuộc về cùng một công ty.
    # Điều này hữu ích khi bạn muốn đảm bảo rằng dữ liệu của bạn được phân tách theo công ty trong môi trường đa công ty.
    _check_company_auto = True
    #... có thể thêm các trường đặc biệt khác như _order, _inherit, _inherits, _check_company_auto,... tùy theo nhu cầu

    # 2. Các trường dữ liệu của model
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda s: s.env.company
    )
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name')
    category_id = fields.Many2one('category', string='Category')
    description = fields.Text(string='Description')
    note = fields.Text(string='Note')

    # Trường compute_field_not_store là một trường được tính toán (computed field) nhưng không được lưu trữ trong cơ sở dữ liệu.
    # Giá trị của trường này sẽ được tính toán mỗi khi có sự thay đổi liên quan đến các trường mà nó phụ thuộc vào (trong trường hợp này là 'name' và 'category_id').
    compute_field_not_store = fields.Char(string='Computed Field Not Stored', compute='_compute_field')

    # Trường compute_field_store là một trường được tính toán và được lưu trữ trong cơ sở dữ liệu.
    # Giá trị của trường này cũng sẽ được tính toán mỗi khi có sự thay đổi liên quan đến các trường mà nó phụ thuộc vào,
    # nhưng giá trị của nó sẽ được lưu trữ trong cơ sở dữ liệu, cho phép truy vấn và sử dụng trong các điều kiện tìm kiếm.
    compute_field_store = fields.Char(string='Stored Computed Field', compute='_compute_field_store', store=True)

    #... có thể thêm các trường khác tùy theo nhu cầu

    # 3. Các ràng buộc cơ sở dữ liệu (SQL constraints)
    _sample_single_code_unique = models.Constraint(
        'unique(company_id, code)',
        _('Sample Single Code must be unique.')
    )
    #... có thể thêm các ràng buộc khác tùy theo nhu cầu

    # 4. Các ràng buộc động (Python constraints). Ràng buộc này sẽ được kiểm tra mỗi khi tạo mới hoặc cập nhật record.
    # Nếu điều kiện trong ràng buộc không được thỏan, một lỗi sẽ được ném ra và hành động sẽ bị hủy bỏ.
    # Trong ví dụ này, ràng buộc đảm bảo rằng trường 'code' không được để trống.
    @api.constrains("code")
    def _check_code(self):
        for rec in self:
            if not rec.code:
                raise UserError(_("Item Code is required."))
    #... có thể thêm các phương thức khác tùy theo nhu cầu

    # 5. Computed methods: Đây là các phương thức được sử dụng để tính toán giá trị của các trường dựa trên các trường khác.
    # Các trường này sẽ được tự động cập nhật mỗi khi có sự thay đổi liên quan đến chúng.
    @api.depends('name', 'category_id')
    def _compute_field(self):
        for rec in self:
            rec.compute_field_not_store = f"{rec.name} - {rec.category_id.name if rec.category_id else 'No Category'}"

    @api.depends('name', 'category_id')
    def _compute_field_store(self):
        for rec in self:
            rec.compute_field_store = f"{rec.name} - {rec.category_id.name if rec.category_id else 'No Category'}"

    # Trường display_name là một trường đặc biệt được sử dụng để thay đổi tên hiển thị của bản ghi trong giao diện người dùng.
    # Override phương thức _compute_display_name để tùy chỉnh cách hiển thị tên của bản ghi dựa trên giá trị của trường 'code' và 'name'.
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
    #... có thể thêm các phương thức khác tùy theo nhu cầu

    # 6. Onchange methods: Đây là các phương thức được gọi khi có sự thay đổi giá trị của một trường nào đó trong giao diện người dùng.
    # Ví dụ, phương thức này sẽ được gọi khi trường 'category_id' thay đổi,
    # và nó sẽ tự động cập nhật trường 'description' dựa trên giá trị của trường 'category_id'.
    @api.onchange("category_id")
    def _onchange_category_id(self):
        if self.category_id:
            self.description = f"Selected category: {self.category_id.name}"
        else:
            self.description = "No category selected"
    #...


    # 7. Override các method của model khi cần thiết, như:
    # create: khi tạo record mới
    # write: khi cập nhật record
    # unlink: khi xóa record

    # Ví dụ, bạn có thể override phương thức create để thêm các xử lý trước khi tạo record mới, như validate dữ liệu hoặc chuẩn bị dữ liệu.
    @api.model_create_multi
    def create(self, vals_list):
        # vals_list là một danh sách các dictionary chứa dữ liệu để tạo các record mới.

        # Xử lý trước khi tạo record (validate, chuẩn bị dữ liệu...)
        # Ví dụ, bạn có thể kiểm tra rằng trường 'name' không được để trống trước khi tạo record mới.
        for val in vals_list:
            if 'name' not in val or not val['name']:
                raise UserError(_("Sample name is required."))
            #... có thể thêm các xử lý khác tùy theo nhu cầu

        # Gọi phương thức create của lớp cha để thực hiện việc tạo record
        return super(SampleSingle, self).create(vals_list)

    def write(self, vals):
        # vals là một dictionary chứa dữ liệu để cập nhật record hiện tại.

        # Xử lý trước khi update record
        # Ví dụ, bạn có thể kiểm tra rằng trường 'name' không được để trống trước khi cập nhật record.
        if 'name' in vals and not vals.get('name'):
            raise UserError(_("Sample name is required."))

        # Ví dụ, bạn có thể tự động cập nhật trường 'note' mỗi khi trường 'name' được cập nhật.
        vals['note'] = f"Record updated with name: {vals.get('name', 'No Name')}"
        #... có thể thêm các xử lý khác tùy theo nhu cầu


        # Gọi phương thức write của lớp cha để thực hiện việc cập nhật record
        result = super(SampleSingle, self).write(vals)

        if result:
            _logger.info("Record updated successfully with values: %s", vals)
            # bạn có thể gửi một thông báo đến người dùng sau khi cập nhật record thành công.
            self.env.user._bus_send(
                "simple_notification",
                {
                    "title": _("Record Updated"),
                    "type": "success",  # info | warning | danger | success
                    "message": "The record has been updated successfully.",

                    # True nếu bạn muốn thông báo dính trên màn hình cho đến khi người dùng đóng nó,
                    # False (mặc định) nếu bạn muốn nó tự động biến mất sau một thời gian ngắn.
                    "sticky": False,
                }
            )
        else:
            _logger.warning("Failed to update record with values: %s", vals)
        return result

    def unlink(self):
        # Xử lý trước khi delete record

        # Ví dự, báo lỗi nếu không còn record nào sau khi xóa.
        if self.search_count([]) == len(self):
            raise UserError(_("Cannot delete all records."))

        # Gọi phương thức unlink của lớp cha để thực hiện việc xóa record
        return super(SampleSingle, self).unlink()

    #...

    # 8. Actions, methods để gọi từ button trên form view hoặc từ các nơi khác trong code.

    # Ví dụ, bạn có thể tạo một method để reset giá trị của trường 'description' về mặc định khi người dùng nhấn một button trên form view.
    def action_reset_description(self):
        """Method này sẽ được gọi khi người dùng nhấn button "Reset Description" trên form view. Nó sẽ reset giá trị của trường 'description' về mặc định."""
        self.ensure_one()
        _logger.info("Reset sample description")
        self.description = "Default description"

        # Sau khi reset description, bạn có thể muốn hiển thị một thông báo cho người dùng biết rằng hành động đã được thực hiện thành công.
        # Dưới đây là cách bạn có thể trả về một action để hiển thị thông báo sau khi reset description:
        return {
            "type": "ir.actions.client",
            'tag': 'display_notification',
            "params": {
                "message": "Description has been reset to default.",
                "type": "success",  # info | warning | danger | success
                "next": {
                    "type": "ir.actions.client",
                    "tag": "soft_reload",  # soft_reload sẽ reload lại view hiện tại mà không cần phải refresh toàn bộ trang
                }
            },
        }

    #... có thể thêm các method khác tùy theo nhu cầu