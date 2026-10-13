from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SampleMultipleLine(models.Model):
    # 1. Các trường đặc biệt của model:
    _name = 'sample.multiple.line'
    _rec_name = 'name'
    _description = 'Sample Multiple Line Description'
    _check_company_auto = True
    #...

    # 2. Các trường dữ liệu của model
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda s: s.env.company
    )
    # Trường sample_multiple_id là một trường Many2one liên kết đến model 'sample.multiple'.
    # Điều này cho phép mỗi bản ghi của SampleMultipleLine có thể liên kết đến một bản ghi của SampleMultiple.
    # Tham số ondelete='cascade' đảm bảo rằng nếu một bản ghi của SampleMultiple bị xóa,
    # tất cả các bản ghi liên quan trong SampleMultipleLine cũng sẽ bị xóa theo.
    # Mặc định ondelete là 'set null', chỉ update sample_multiple_id thành null khi record cha bị xóa.
    sample_multiple_id = fields.Many2one('sample.multiple', string='Sample Multiple', ondelete='cascade')
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    #...

    # 3. Các ràng buộc cơ sở dữ liệu (SQL constraints)
    _sample_multiple_line_code_unique = models.Constraint(
        'unique(company_id, sample_multiple_id, code)',
        _('Sample Multiple Line must be unique.')
    )
    #...

    # 5. Computed methods
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
    #...

    # 7. Override method
    def unlink(self):
        # Xử lý trước khi delete record

        # Ví dự, báo lỗi nếu không còn record nào sau khi xóa.
        if self.search_count([('sample_multiple_id','=',self.sample_multiple_id)]) == len(self):
            raise UserError(_("Cannot delete all records."))

        # Gọi phương thức unlink của lớp cha để thực hiện việc xóa record
        return super(SampleMultipleLine, self).unlink()

    #...

    # 8. Actions methods
    def action_reset_description(self):
        """Method này sẽ được gọi khi người dùng nhấn button "Reset Description" trên form view. Nó sẽ reset giá trị của trường 'description' về mặc định."""
        self.ensure_one()
        _logger.info("Reset sample description")
        self.description = "Default description"

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

    #...
