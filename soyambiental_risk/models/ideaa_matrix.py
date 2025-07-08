from odoo import api, fields, models
from odoo.exceptions import UserError


class IDEAAMatrix(models.Model):
    _name = 'sga.ideaa_matrix'
    _inherit = ['mgmtsystem.validation.mail', 'model.origin.abstract', 'mgmtsystem.code']
    _description = 'Matriz de identificación de aspectos ambientales'

    name = fields.Char(string='Nombre')

    stage_ids = fields.One2many('sga.matrix.stage', 'stage_ideaa_matrix_id', string='Etapas')
    stage_process_ids = fields.One2many('sga.matrix.stage_process', 'process_ideaa_matrix_id', string='Procesos')
    process_aspect_impact_ids = fields.One2many('sga.matrix.process', 'ideaa_matrix_id', string='Aspectos e impactos')
    evaluation_id = fields.Many2one('sga.matrix.evaluation', string='Evaluación')
    process_evaluation_ids = fields.One2many('sga.matrix.process', 'ideaa_matrix_id', string='Evaluación de impactos')
    process_control_ids = fields.One2many('sga.matrix.process', 'ideaa_matrix_id', string='Controles')
    survey_ids = fields.Many2many('survey.survey', string='Encuestas')
    survey_count = fields.Integer(compute='_compute_survey_count', string='# Encuestas')

    @api.depends('survey_ids')
    def _compute_survey_count(self):
        for record in self:
            record.survey_count = len(record.survey_ids)

    def action_open_survey(self):
        self.ensure_one()
        action = self.env.ref('survey.action_survey_form').read()[0]
        action['domain'] = [('id', 'in', self.survey_ids.ids)]
        return action

    matrix_state = fields.Selection([
        ('draft', 'Borrador'),
        ('process', 'Proceso'),
        ('identification', 'Identificación'),
        ('evaluation', 'Evaluación'),
        ('control', 'Controles'),
    ], string='Estado', default='draft', copy=False)

    def init_preparation(self):
        for each in self:
            each.matrix_state = 'process'
            vals = []
            for stage in self.stage_ids:
                for activity in stage.activity_ids:
                    for task in activity.task_ids:
                        line = {
                            'stage_id': stage.id,
                            'activity_id': activity.id,
                            'task_id': task.id,
                            'job_ids': [(6, 0, task.job_ids.ids)],
                        }
                        vals.append((0, 0, line))
            each.stage_process_ids = vals

    def action_identify_aspect_impact(self):
        for each in self:
            each.matrix_state = 'identification'
            vals = []
            for stage_process in each.stage_process_ids:
                line = {
                    'stage_id': stage_process.stage_id.id,
                    'activity_id': stage_process.activity_id.id,
                    'task_id': stage_process.task_id.id,
                    'job_ids': [(6, 0, stage_process.job_ids.ids)],
                }
                vals.append((0, 0, line))
            each.process_aspect_impact_ids = vals

    def evaluate_impacts(self):
        for each in self:
            if not each.evaluation_id:
                raise UserError('Ingrese una evaluación primero')
            each.matrix_state = 'evaluation'
            for ev in each.process_evaluation_ids:
                ev.evaluation_ids = [(5, 0, 0)]
                vals = []
                for val in each.evaluation_id.item_ids:
                    line = {
                        'evaluation_item_id': val.id,
                    }
                    vals.append((0, 0, line))
                ev.evaluation_ids = vals

    def controlate_risks(self):
        """
        Añade datos al campo de control de riesgos y cambia el estado a controles
        """
        for each in self:
            each.matrix_state = 'control'
            each.process_control_ids = [(6, 0, each.process_evaluation_ids.ids)]
            for ev in each.process_control_ids:
                vals = []
                for val in each.evaluation_id.item_ids:
                    line = {
                        'name': val.name,
                        'item_id': val.id,
                        'evaluation_id': each.evaluation_id.id,
                    }
                    vals.append((0, 0, line))
                #ev.control_item_ids = vals
