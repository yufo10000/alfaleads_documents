from odoo import models, fields, api, _


class DocumentFolder(models.Model):
    _inherit = 'documents.folder'

    full_path = fields.Char(compute='_compute_full_path')

    @api.depends('parent_folder_id', 'name')
    def _compute_full_path(self):
        self.full_path = self._get_full_path()

    def _get_full_path(self, path=None):

        """
        Recursively get the names of all parent folders.
        If the name is already formed, then return it with
        the name of the current folder
        """
        if path is None:
            path = []
        path.append(self.name)
        if not self.parent_folder_id:
            return ' / '.join(path[::-1])
        else:
            return self.parent_folder_id._get_full_path(path)
