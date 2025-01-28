from odoo import api, fields, models
from odoo.exceptions import UserError


class MatrixProcessEvaluationControl(models.Model):
    _name = 'sga.matrix.process.evaluation_control'
    _description = 'Evaluación y control'

    evaluation_item_id = fields.Many2one('sga.matrix.evaluation.item', string='Factor')
    evaluation_item_criterio_id = fields.Many2one('sga.matrix.evaluation.item.criterio', string='Criterio', domain="[('item_id', '=', evaluation_item_id)]")
    evaluation_value_id = fields.Many2one('sga.matrix.evaluation.item.value', string='Valor', domain="[('item_id', '=', evaluation_item_id)]")
    evaluation_process_id = fields.Many2one('sga.matrix.process', string='Proceso de la matriz SGA (Evaluación)')
    reevaluation_process_id = fields.Many2one('sga.matrix.process', string='Proceso de la matriz SGA (Reevaluación)')

    @api.onchange('evaluation_item_criterio_id')
    def _onchange_evaluation_item_criterio_id(self):
        for record in self:
            if record.evaluation_item_criterio_id:
                record.evaluation_value_id = record.evaluation_item_criterio_id.item_value_id


class MatrixStageTask(models.Model):
    _name = 'sga.matrix.stage.task'
    _description = 'Tarea'

    name = fields.Char(string='Tarea')
    job_ids = fields.Many2many('hr.job', string='Puestos de trabajo')
    activity_id = fields.Many2one('sga.matrix.stage.activity', string='Actividad')


class MatrixStageActivity(models.Model):
    _name = 'sga.matrix.stage.activity'
    _description = 'Actividad'

    name = fields.Char(string='Actividad')
    task_ids = fields.One2many('sga.matrix.stage.task', 'activity_id', string='Tareas')
    stage_id = fields.Many2one('sga.matrix.stage', string='Etapa')


class MatrixStage(models.Model):
    _name = 'sga.matrix.stage'
    _description = 'Etapa'

    name = fields.Char(string='Etapa')
    activity_ids = fields.One2many('sga.matrix.stage.activity', 'stage_id', string='Actividades')

    stage_ideaa_matrix_id = fields.Many2one('sga.ideaa_matrix', string='Matriz')


class MatrixImpact(models.Model):
    _name = 'sga.matrix.impact'
    _description = 'Impactos'

    name = fields.Char('Nombre')

    sql_constraints = [
        ('name_uniq', 'unique (name)', 'El impacto ya existe!'),
    ]


class MatrixStageProcess(models.Model):
    _name = 'sga.matrix.stage_process'
    _description = 'Proceso de la matriz SGA'

    name = fields.Char(string='Etapa')
    stage_id = fields.Many2one('sga.matrix.stage', string='Etapa')
    activity_id = fields.Many2one('sga.matrix.stage.activity', string='Actividad')
    task_id = fields.Many2one('sga.matrix.stage.task', string='Tarea')
    job_ids = fields.Many2many('hr.job', string='Puestos de trabajo')

    process_ideaa_matrix_id = fields.Many2one('sga.ideaa_matrix', string='Matriz')


class MatrixAspect(models.Model):
    _name = 'sga.matrix.aspect'
    _description = 'Aspectos'

    name = fields.Char('Nombre')

    sql_constraints = [
        ('name_uniq', 'unique (name)', 'El aspecto ya existe!'),
    ]


class MatrixProcess(models.Model):
    _name = 'sga.matrix.process'
    _description = 'Evaluación de impacto'

    name = fields.Char(string='Impacto')
    ideaa_matrix_id = fields.Many2one('sga.ideaa_matrix', string='Matriz')
    ideaa_matrix2_id = fields.Many2one('sga.ideaa_matrix', string='Matriz')
    ideaa_matrix3_id = fields.Many2one('sga.ideaa_matrix', string='Matriz')
    ideaa_matrix4_id = fields.Many2one('sga.ideaa_matrix', string='Matriz')

    aspect_ids = fields.Many2many('sga.matrix.aspect', string='Aspectos')
    impact_ids = fields.Many2many('sga.matrix.impact', string='Impactos')
    legal_ids = fields.Many2many('legal.legal', string='Requisito legal')

    stage_id = fields.Many2one('sga.matrix.stage', string='Etapa')
    activity_id = fields.Many2one('sga.matrix.stage.activity', string='Actividad')
    task_id = fields.Many2one('sga.matrix.stage.task', string='Tarea')
    job_ids = fields.Many2many('hr.job', string='Puestos de trabajo')

    evaluation_ids = fields.One2many('sga.matrix.process.evaluation_control', 'evaluation_process_id', string='Evaluación')
    evaluation_p = fields.Integer(compute='_compute_risk_valuation', string='Nivel de probabilidad (P)')
    evaluation_c = fields.Integer(compute='_compute_risk_valuation', string='Nivel de consecuencia (C)')
    evaluation_pxc = fields.Integer(compute='_compute_risk_valuation', string='Valoración del riesgo (P x C)')
    level = fields.Char(string='Nivel de riesgo puro',compute='_compute_risk_valuation')
    process_id = fields.Many2one('process.edition', string='Proceso')
    interpretation = fields.Text(string='Interpretación')

    risk_ids = fields.Many2many(
        'matrix.block.line',
        relation='sga_matrix_process_risk_rel',
        column1='risk_id',
        column2='matrix_process_id',
        string='Riesgos',
        domain=[('type', '=', 'risk')],
    )
    opp_ids = fields.Many2many(
        'matrix.block.line',
        relation='sga_matrix_process_opp_rel',
        column1='opp_id',
        column2='matrix_process_id',
        string='Oportunidades',
        domain=[('type', '=', 'opportunity')],
    )

    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')
    reevaluation_ids = fields.One2many('sga.matrix.process.evaluation_control', 'reevaluation_process_id', string='Reevaluación')
    control_p = fields.Integer(compute='_compute_control_pxc', string='Reevaluación de riesgos P')
    control_c = fields.Integer(compute='_compute_control_pxc', string='Reevaluación de riesgos C')
    control_pxc = fields.Integer(compute='_compute_control_pxc', string='Reevaluación de riesgos PxC')
    control_level = fields.Char(compute='_compute_control_pxc', string='Nivel de riesgo residual')

    @api.depends('reevaluation_ids')
    def _compute_risk_valuation(self):
        for each in self:
            p_value = None
            c_value = None
            r_value = 0
            for item in each.evaluation_ids:
                if item.evaluation_item_id.name == 'Probabilidad de ocurrencia' and item.evaluation_value_id:
                    p_value = int(item.evaluation_value_id.value)
                if item.evaluation_item_id.name == 'Consecuencia' and item.evaluation_value_id:
                    c_value = int(item.evaluation_value_id.value)
            if p_value and c_value:
                r_value = p_value * c_value
                if r_value > 7:
                    each.level = 'Alto'
                elif p_value == 1 and c_value == 3:
                    each.level = 'Medio'
                elif p_value < 3 and c_value > 2:
                    each.level = 'Monitoreable'
                elif r_value == 4 or (p_value == 3 and c_value == 2):
                    each.level = 'Medio'
                else:
                    each.level = 'Bajo'
            else:
                each.level = ''
            each.evaluation_p = p_value
            each.evaluation_c = c_value
            each.evaluation_pxc = r_value

    @api.depends('reevaluation_ids')
    def _compute_control_pxc(self):
        for each in self:
            p_value = None
            c_value = None
            r_value = 0
            for item in each.reevaluation_ids:
                if item.evaluation_item_id.name == 'Probabilidad de ocurrencia' and item.evaluation_value_id:
                    p_value = int(item.evaluation_value_id.value)
                if item.evaluation_item_id.name == 'Consecuencia' and item.evaluation_value_id:
                    c_value = int(item.evaluation_value_id.value)
            if p_value and c_value:
                r_value = p_value * c_value
                if r_value > 7:
                    each.control_level = 'Alto'
                elif p_value == 1 and c_value == 3:
                    each.control_level = 'Medio'
                elif p_value < 3 and c_value > 2:
                    each.control_level = 'Monitoreable'
                elif r_value == 4 or (p_value == 3 and c_value == 2):
                    each.control_level = 'Medio'
                else:
                    each.control_level = 'Bajo'
            else:
                each.control_level = None

            each.control_pxc = r_value
            each.control_p = p_value
            each.control_c = c_value
