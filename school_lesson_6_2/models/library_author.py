from datetime import timedelta
from odoo import fields, models, _
from odoo.exceptions import UserError


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Book Authors'

    first_name = fields.Char(required=True,
                             translate=True)
    last_name = fields.Char(required=True,
                            translate=True)
    birth_date = fields.Date('Birthday')

    def name_get(self):
        return [(rec.id, "%s %s" % (
            rec.first_name, rec.last_name)) for rec in self]

    def action_delete(self):
        self.ensure_one()
        self.check_access_rights('unlink')
        self.unlink()

    def _create_by_user(self, vals):
        return self.sudo().create(vals)

    def write(self, vals):
        result = fields.Datetime.now() - timedelta(days=30)
        if result > self.create_date and not self.env.user.has_group(
                'school_lesson_6_2.group_library_admin'):
            raise UserError(_("You cannot make changes to the Author "
                              "since 30 days have passed "
                              "since the creation date."))
        return super(LibraryAuthor, self).write(vals)
