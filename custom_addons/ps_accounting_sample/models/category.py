from odoo import fields, models, api

class Category(models.Model):
    _name = 'category'
    _description = 'Category'

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            if rec.code and rec.name:
                rec.display_name = f'[{rec.code}] {rec.name}'
            else:
                rec.display_name = ""
