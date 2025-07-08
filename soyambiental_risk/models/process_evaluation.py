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

    # Campo computed para controlar readonly
    criterio_readonly = fields.Boolean(compute='_compute_criterio_readonly', store=False)

    @api.depends('evaluation_item_id', 'evaluation_item_id.has_criterios')
    def _compute_criterio_readonly(self):
        for record in self:
            # Si no hay item seleccionado o el item no tiene criterios, hacer readonly
            record.criterio_readonly = not record.evaluation_item_id or not record.evaluation_item_id.has_criterios

    @api.onchange('evaluation_item_id')
    def _onchange_evaluation_item_id(self):
        # Limpiar el criterio si el item no tiene criterios
        if self.evaluation_item_id and not self.evaluation_item_id.has_criterios:
            self.evaluation_item_criterio_id = False
    
    
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

    evaluation_ids = fields.One2many('sga.matrix.process.evaluation_control', 'evaluation_process_id', string='Evaluación' , default=lambda self: self._get_default_evaluation_records())
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
    reevaluation_ids = fields.One2many('sga.matrix.process.evaluation_control', 'reevaluation_process_id', string='Reevaluación' , default=lambda self: self._get_default_reevaluation_records())
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

    ## default evaluations

    def _get_default_evaluation_records(self):
        """
        Retorna los registros por defecto para evaluation_ids
        """
        default_evaluations = [
            # Registro 1
            {
                'evaluation_item_id': 'soyambiental_risk.evaluation_item_1',
                'evaluation_item_criterio_id': False,
            },
            # Registro 2
            {
                'evaluation_item_id': 'soyambiental_risk.evaluation_item_2',
                'evaluation_item_criterio_id': 'soyambiental_risk.evaluation_item2_criterio1',
            },
            # Registro 3
            {
                'evaluation_item_id': 'soyambiental_risk.evaluation_item_2',
                'evaluation_item_criterio_id': 'soyambiental_risk.evaluation_item2_criterio2',
            },
            # Registro 4
            {
                'evaluation_item_id': 'soyambiental_risk.evaluation_item_2',
                'evaluation_item_criterio_id': 'soyambiental_risk.evaluation_item2_criterio3',
            },
            # Registro 5
            {
                'evaluation_item_id': 'soyambiental_risk.evaluation_item_2',
                'evaluation_item_criterio_id': 'soyambiental_risk.evaluation_item2_criterio4',
            },
            # Registro 6
            {
                'evaluation_item_id': 'soyambiental_risk.evaluation_item_2',
                'evaluation_item_criterio_id': 'soyambiental_risk.evaluation_item2_criterio5',
            },
        ]
        
        evaluation_vals = []
        for eval_data in default_evaluations:
            try:
                # Resolver las referencias XML ID
                item_id = self.env.ref(eval_data['evaluation_item_id']).id
                criterio_id = False
                if eval_data['evaluation_item_criterio_id']:
                    criterio_id = self.env.ref(eval_data['evaluation_item_criterio_id']).id
                
                line = {
                    'evaluation_item_id': item_id,
                    'evaluation_item_criterio_id': criterio_id,
                }
                evaluation_vals.append((0, 0, line))
            except ValueError:
                # Si alguna referencia no existe, continuar sin agregar ese registro
                continue
        
        return evaluation_vals
    
    def _get_default_reevaluation_records(self):
        """
        Retorna el registro por defecto para reevaluation_ids
        """
        try:
            item_id = self.env.ref('soyambiental_risk.evaluation_item_1').id
            line = {
                'evaluation_item_id': item_id,
                'evaluation_item_criterio_id': False,
            }
            item2_id = self.env.ref('soyambiental_risk.evaluation_item_2').id
            line2 = {
                'evaluation_item_id': item2_id,
                'evaluation_item_criterio_id': False,
            }
            return [(0, 0, line), (0, 0, line2)]
        except ValueError:
            return []


    @api.model_create_multi
    def create(self, vals_list):
        """
        Override del método create para añadir automáticamente
        los registros por defecto en evaluation_ids
        """
        # Procesar cada registro a crear
        for vals in vals_list:
            # Solo añadir los registros por defecto si evaluation_ids no está ya definido
            if 'evaluation_ids' not in vals or not vals['evaluation_ids']:
                vals['evaluation_ids'] = self._get_default_evaluation_records()
            if 'reevaluation_ids' not in vals or not vals['reevaluation_ids']:
                vals['reevaluation_ids'] = self._get_default_reevaluation_records()


        # Crear los registros
        records = super(MatrixProcess, self).create(vals_list)
        
        return records
    
    @api.model
    def default_get(self, fields_list):
        """
        Override del método default_get para asegurar que los valores por defecto
        se establezcan correctamente cuando se crean registros desde One2many
        """
        defaults = super(MatrixProcess, self).default_get(fields_list)
        
        # Si evaluation_ids está en la lista de campos y no tiene valor por defecto
        if 'evaluation_ids' in fields_list and 'evaluation_ids' not in defaults:
            defaults['evaluation_ids'] = self._get_default_evaluation_records()

        if 'reevaluation_ids' in fields_list and 'reevaluation_ids' not in defaults:
            defaults['reevaluation_ids'] = self._get_default_reevaluation_records()

        return defaults