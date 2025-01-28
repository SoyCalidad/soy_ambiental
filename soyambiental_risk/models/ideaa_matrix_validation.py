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

    def clear_old_edition(self, edition):
        for s in edition.stage_ids:
            s.unlink()
        for s in edition.detail_ids:
            s.unlink()
        for s in edition.dangerrisk_ids:
            s.unlink()
        for s in edition.evaluation_ids:
            s.unlink()
        for s in edition.control_ids:
            s.unlink()

    def _copy_edition(self):
        new_edition = self.copy({
            'version': self.version,
            'deactivate_date': fields.Date.today(),
            'parent_edition': self.id,
            'state': 'validate_ok',
            'matrix_state': 'control',
        })
        return new_edition

    def button_new_version(self):
        self.ensure_one()
        old_edition = self._copy_edition()
        for stg in self.stage_ids:
            dict_stg = {
                'name': stg.name,
                'stage_ideaa_matrix_id': old_edition.id,
            }
            new_stg = self.env['sga.matrix.stage'].create(dict_stg)
            for act in stg.activity_ids:
                dict_act = {
                    'name': act.name,
                    'stage_id': new_stg.id,
                }
                new_act = self.env['sga.matrix.stage.activity'].create(dict_act)
                for task in act.task_ids:
                    dict_task = {
                        'name': task.name,
                        'job_ids': [(6, 0, task.job_ids.ids)],
                        'activity_id': new_act.id,
                    }
                    self.env['sga.matrix.stage.task'].create(dict_task)
        for det in self.process_aspect_impact_ids:
            new = {
                'stage_id': det.stage_id.id,
                'activity_id': det.activity_id.id,
                'job_ids': [(6, 0, det.job_ids.ids)],
                'task_id': det.task_id.id,
                'aspect_ids': [(6, 0, det.aspect_ids.ids)],
                'impact_ids': [(6, 0, det.impact_ids.ids)],
                'ideaa_matrix2_id': old_edition.id,
            }
            self.env['sga.matrix.process'].create(new)
        for ev in self.process_evaluation_ids:
            new = {
                'name': ev.name,
                'stage_id': ev.stage_id.id,
                'activity_id': ev.activity_id.id,
                'job_ids': [(6, 0, ev.job_ids.ids)],
                'task_id': ev.task_id.id,
                'aspect_ids': [(6, 0, ev.aspect_ids.ids)],
                'impact_ids': [(6, 0, ev.impact_ids.ids)],
                'interpretation': ev.interpretation,
                'process_id': ev.process_id.id,
                'ideaa_matrix3_id': old_edition.id,
            }
            new_ev = self.env['sga.matrix.process'].create(new)
            for item in ev.evaluation_ids:
                new_ = {
                    'name': item.evaluation_value_id.name,
                    'value_id': item.evaluation_value_id.id,
                    'evaluation_process_id': new_ev.id,
                }
                self.env['sga.matrix.process.evaluation_control'].create(new_)
        for con in self.process_control_ids:
            new = {
                'name': con.name,
                'stage_id': con.stage_id.id,
                'activity_id': con.activity_id.id,
                'job_ids': [(6, 0, con.job_ids.ids)],
                'task_id': con.task_id.id,
                'aspect_ids': [(6, 0, con.aspect_ids.ids)],
                'impact_ids': [(6, 0, con.impact_ids.ids)],
                'interpretation': con.interpretation,
                'process_id': con.process_id.id,
                'action_ids': [(6, 0, con.action_ids.ids)],
                'ideaa_matrix4_id': old_edition.id
            }
            con_new = self.env['sga.matrix.process'].create(new)
            for con_ in con.reevaluation_ids:
                new_con_ = {
                    'name': con_.evaluation_item_id.name,
                    'reevaluation_process_id': con_new.id,
                }
                self.env['sst.risk_matrix.evaluation.control'].create(new_con_)

        revno = self.version
        self.remove_validation_steps_users()
        self.write({
            'version': revno + 1,
            'state': 'elaborate',
            'matrix_state': 'draft',
            'name': self.name
        })
        self.stage_process_ids = None
        self.process_aspect_impact_ids = None
        self.process_evaluation_ids = None
        self.process_control_ids = None

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
