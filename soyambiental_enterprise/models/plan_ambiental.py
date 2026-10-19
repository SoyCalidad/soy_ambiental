from odoo import api, fields, models


class PlanAmbiental(models.Model):
    _inherit = 'plan.ambiental'

    document = fields.Many2many(
        comodel_name='documents.document',
        relation='relation_document',
        string='Documentos',
        domain=[('type', '=', 'binary')],
    )
    document_counts = fields.Char(
        compute='_compute_document_counts', string='Cantidad de documentos')

    @api.depends('document')
    def _compute_document_counts(self):
        for each in self:
            each.document_counts = len(each.document)

    def openviews(self):
        if self._context.get('type_action', '') == 'document':
            action_rec = self.env.ref(
                'documents.document_action').read()[0]
            action_rec['domain'] = [('id', 'in', self.document.ids)]
            return action_rec
        return super().openviews()
