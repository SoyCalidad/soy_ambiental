from odoo import api, fields, models


class ProgramaAmbiental(models.Model):
    _inherit = 'programa.ambiental'

    documents = fields.Many2many(
        comodel_name='documents.document',
        relation='relation_documents',
        string='Documentos',
        domain=[('type', '=', 'binary')],
    )
    documents_counts = fields.Char(
        compute='_compute_documents_counts', string='Cantidad de documentos')

    @api.depends('documents')
    def _compute_documents_counts(self):
        for each in self:
            each.documents_counts = len(each.documents)

    def openviews(self):
        if self._context.get('type_action', '') == 'documents':
            action_rec = self.env.ref(
                'documents.document_action').read()[0]
            action_rec['domain'] = [('id', 'in', self.documents.ids)]
            return action_rec
        return super().openviews()
