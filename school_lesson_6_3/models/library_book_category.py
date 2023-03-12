from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    """this class is a category of books"""

    _name = 'library.book.category'
    _description = 'Book Category'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(index=True, required=True)
    # this is category name
    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True,
        store=True)
    parent_id = fields.Many2one(
        comodel_name='library.book.category',
        string='Parent Category',
        index=True,
        ondelete='cascade')
    child_id = fields.One2many(
        comodel_name='library.book.category',
        inverse_name='parent_id',
        string='Child Categories')
    parent_path = fields.Char(index=True)
    book_count = fields.Integer(compute='_compute_book_count')
    # displays the number of books in a category

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        """creating a hierarchical category name"""
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _compute_book_count(self):
        for obj in self:
            obj.book_count = self.env[
                'library.book'].search_count([
                ('category_id', 'child_of', obj.id)
            ])

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        """necessary to avoid creating a recursive category"""
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursion categories.'))

    def get_category_books(self):
        """method that returns a list of all the books in the current category"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "library.book",
            "domain": [("category_id", "=", self.id)],
            "name": "Books",
            "view_mode": "tree",
        }
