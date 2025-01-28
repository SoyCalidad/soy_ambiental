from odoo import api, fields, models


class InternalIssue(models.Model):
    _name = 'mgmtsystem.context.internal_issue'
    _inherit = ['mgmtsystem.context.internal_issue', 'sga.abstract']

    sga_scope = fields.Text(string='Alcance del sistema de gestión ambiental')

    @api.onchange('sga_scope')
    def _onchange_quality_scope(self):
        for each in self:
            each.scope = each.sga_scope
