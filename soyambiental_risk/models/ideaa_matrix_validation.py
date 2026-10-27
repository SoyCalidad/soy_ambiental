from odoo import api, fields, models


class MatrixMatrix(models.Model):
    _inherit = 'sga.ideaa_matrix'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'sga_ideaa_matrix_elaboration_id', string='Elaboración', copy=True)
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'sga_ideaa_matrix_review_id', string='Revisión', copy=True)
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'sga_ideaa_matrix_validation_id', string='Validación', copy=True)

    parent_edition = fields.Many2one(
        comodel_name='sga.ideaa_matrix', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='sga.ideaa_matrix', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def _copy_edition(self):
        new_edition = self.copy({
            'version': self.version,
            'deactivate_date': fields.Date.today(),
            'parent_edition': self.id,
            'state': 'validate_ok',
        })
        return new_edition

    def button_new_version(self):
        self.ensure_one()
        self._copy_edition()
        revno = self.version
        self.remove_validation_steps_users()
        self.write({
            'version': revno + 1,
            'state': 'elaborate',
            'name': self.name
        })

    def action_open_older_versions(self):
        result = self.env.ref('soyambiental_risk.sga_ideaa_matrix_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class MatrixValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    sga_ideaa_matrix_elaboration_id = fields.Many2one('sga.ideaa_matrix', string='Padre (Elaboración de Matriz SGA)')
    sga_ideaa_matrix_review_id = fields.Many2one('sga.ideaa_matrix', string='Padre (Revisión de Matriz SGA)')
    sga_ideaa_matrix_validation_id = fields.Many2one('sga.ideaa_matrix', string='Padre (Validación de Matriz SGA)')
