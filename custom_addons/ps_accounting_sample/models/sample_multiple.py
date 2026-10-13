from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class SampleMultiple(models.Model):
    # 1. Các trường đặc biệt của model:
    _name = 'sample.multiple'
    _rec_name = 'name'
    _description = 'Sample Multiple Description'
    _check_company_auto = True
    #...

    # 2. Các trường dữ liệu của model
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda s: s.env.company
    )
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    category_id = fields.Many2one('category', string='Category')
    description = fields.Text(string='Description')
    note = fields.Text(string='Note')

    # Trường line_ids là một trường One2many liên kết đến model 'sample.multiple.line'.
    # Điều này cho phép mỗi bản ghi của SampleMultiple có thể liên kết đến nhiều bản ghi của SampleMultipleLine.
    line_ids = fields.One2many('sample.multiple.line', 'sample_multiple_id', string='Sample Multiple Lines')

    #...

    # 3. Các ràng buộc cơ sở dữ liệu (SQL constraints)
    _sample_multiple_code_unique = models.Constraint(
        'unique(company_id, code)',
        _('Sample Multiple Code must be unique.')
    )
    #...

    # 7. Override method
    def unlink(self):
        # Xử lý trước khi delete record

        # Ví dụ, báo lỗi nếu record có liên kết với các dòng trong SampleMultipleLine.
        # Điều này sẽ ngăn người dùng xóa một bản ghi của SampleMultiple nếu nó vẫn còn các bản ghi liên quan trong SampleMultipleLine.
        if len(self.line_ids):
            raise UserError(_("Cannot delete record because it has related lines. Please delete the related lines first."))

        # Gọi phương thức unlink của lớp cha để thực hiện việc xóa record
        return super(SampleMultiple, self).unlink()

    #...

    # 8. Actions methods
    def action_line_count(self):
        """Action method để đếm số lượng dòng liên quan trong SampleMultipleLine và cập nhật thông tin này vào trường note của SampleMultiple."""
        self.ensure_one()
        _logger.info("Calculating line count for SampleMultiple with Code: %s", self.code)

        # Sử dụng phương thức search_count để đếm số lượng bản ghi trong model 'sample.multiple.line' có trường 'sample_multiple_id' bằng với id của bản ghi hiện tại.
        line_count = self.env['sample.multiple.line'].search_count([('sample_multiple_id', '=', self.id)])
        self.note = f"This sample has {line_count} related lines."

        return {
            "type": "ir.actions.client",
            'tag': 'display_notification',
            "params": {
                "message": "Line count has been updated in the note field.",
                "type": "success",  # info | warning | danger | success
                "next": {
                    "type": "ir.actions.client",
                    "tag": "soft_reload",  # soft_reload sẽ reload lại view hiện tại mà không cần phải refresh toàn bộ trang
                }
            },
        }

    #...
