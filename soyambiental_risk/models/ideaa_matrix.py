from odoo import api, fields, models
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

LEVEL_SELECTION = [
    ('1', 'Baja (1)'),
    ('3', 'Media (3)'),
    ('5', 'Alta (5)'),
]

CONDITION_SELECTION = [
    ('normal', 'Normal'),
    ('abnormal', 'Anormal'),
    ('emergency', 'Emergencia'),
]

SIGNIFICANCE_SELECTION = [
    ('not_significant', 'No Significativo (NS)'),
    ('significant', 'Significativo (S)'),
]

# Nivel de impacto (F x S x A) a partir del cual el aspecto es significativo
SIGNIFICANCE_THRESHOLD = 27


def compute_impact_level(frequency, severity, scope):
    """Nivel de impacto = Frecuencia x Severidad x Alcance (0 si falta alguno)."""
    if not (frequency and severity and scope):
        return 0
    return int(frequency) * int(severity) * int(scope)


def compute_significance(impact_level):
    if not impact_level:
        return False
    return 'significant' if impact_level >= SIGNIFICANCE_THRESHOLD else 'not_significant'


class IDEAAMatrix(models.Model):
    _name = 'sga.ideaa_matrix'
    _inherit = ['mgmtsystem.validation.mail', 'model.origin.abstract', 'mgmtsystem.code']
    _description = 'Matriz de identificación de aspectos ambientales'

    name = fields.Char(string='Nombre')

    line_ids = fields.One2many('sga.ideaa_matrix.line', 'matrix_id', string='Matriz', copy=True)
    survey_ids = fields.Many2many('survey.survey', string='Encuestas')
    survey_count = fields.Integer(compute='_compute_survey_count', string='# Encuestas')

    # Campos de captura de la página "Datos". Al pulsar "Agregar" se copian
    # como una nueva línea de la página "Matriz" y se limpian.
    eval_stage = fields.Char(string='Etapa del ciclo de vida', copy=False)
    eval_process = fields.Char(string='Proceso', copy=False)
    eval_activity = fields.Char(string='Actividad', copy=False)
    eval_aspect = fields.Char(string='Aspecto Ambiental', copy=False)
    eval_impact = fields.Char(string='Impacto Ambiental', copy=False)
    eval_condition = fields.Selection(CONDITION_SELECTION, string='Condición', copy=False)
    eval_controls = fields.Text(string='Controles', copy=False)
    eval_frequency = fields.Selection(LEVEL_SELECTION, string='Frecuencia', copy=False)
    eval_severity = fields.Selection(LEVEL_SELECTION, string='Severidad', copy=False)
    eval_scope = fields.Selection(LEVEL_SELECTION, string='Alcance', copy=False)
    eval_impact_level = fields.Integer(string='Nivel de Impacto', compute='_compute_eval_significance')
    eval_significance = fields.Selection(
        SIGNIFICANCE_SELECTION, string='Nivel de Significancia', compute='_compute_eval_significance')
    eval_action_ids = fields.Many2many(
        'mgmtsystem.action',
        relation='sga_ideaa_matrix_eval_action_rel',
        column1='matrix_id',
        column2='action_id',
        string='Medidas de control para implementar',
        copy=False,
    )

    lines_locked = fields.Boolean(compute='_compute_lines_locked')

    @api.depends('state', 'can_edit_form')
    def _compute_lines_locked(self):
        """La matriz solo se edita mientras se elabora o revisa (salvo que se permita editar siempre)."""
        for each in self:
            each.lines_locked = each.state in ('validate', 'validate_ok', 'cancel') and not each.can_edit_form

    @api.depends('eval_frequency', 'eval_severity', 'eval_scope')
    def _compute_eval_significance(self):
        for each in self:
            level = compute_impact_level(each.eval_frequency, each.eval_severity, each.eval_scope)
            each.eval_impact_level = level
            each.eval_significance = compute_significance(level)

    @api.depends('survey_ids')
    def _compute_survey_count(self):
        for record in self:
            record.survey_count = len(record.survey_ids)

    def action_open_survey(self):
        self.ensure_one()
        action = self.env.ref('survey.action_survey_form').read()[0]
        action['domain'] = [('id', 'in', self.survey_ids.ids)]
        return action

    def action_add_line(self):
        """Agrega los datos capturados en la página "Datos" como línea de la matriz."""
        self.ensure_one()
        required = {
            'eval_stage': 'Etapa del ciclo de vida',
            'eval_process': 'Proceso',
            'eval_activity': 'Actividad',
            'eval_aspect': 'Aspecto Ambiental',
            'eval_impact': 'Impacto Ambiental',
            'eval_condition': 'Condición',
        }
        missing = [label for fname, label in required.items() if not self[fname]]
        if missing:
            raise UserError('Complete los siguientes campos antes de agregar:\n- ' + '\n- '.join(missing))
        self.write({
            'line_ids': [(0, 0, {
                'stage': self.eval_stage,
                'process': self.eval_process,
                'activity': self.eval_activity,
                'aspect': self.eval_aspect,
                'impact': self.eval_impact,
                'condition': self.eval_condition,
                'controls': self.eval_controls,
                'frequency': self.eval_frequency,
                'severity': self.eval_severity,
                'scope': self.eval_scope,
                'action_ids': [(6, 0, self.eval_action_ids.ids)],
            })],
            'eval_stage': False,
            'eval_process': False,
            'eval_activity': False,
            'eval_aspect': False,
            'eval_impact': False,
            'eval_condition': False,
            'eval_controls': False,
            'eval_frequency': False,
            'eval_severity': False,
            'eval_scope': False,
            'eval_action_ids': [(5, 0, 0)],
        })


class IDEAAMatrixLine(models.Model):
    _name = 'sga.ideaa_matrix.line'
    _description = 'Línea de la matriz de identificación de aspectos ambientales'
    _order = 'sequence, id'

    matrix_id = fields.Many2one('sga.ideaa_matrix', string='Matriz', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Secuencia', default=10)

    stage = fields.Char(string='Etapa del ciclo de vida')
    process = fields.Char(string='Proceso')
    activity = fields.Char(string='Actividad')
    aspect = fields.Char(string='Aspecto Ambiental')
    impact = fields.Char(string='Impacto Ambiental')
    condition = fields.Selection(CONDITION_SELECTION, string='Condición')
    controls = fields.Text(string='Controles')
    frequency = fields.Selection(LEVEL_SELECTION, string='Frecuencia')
    severity = fields.Selection(LEVEL_SELECTION, string='Severidad')
    scope = fields.Selection(LEVEL_SELECTION, string='Alcance')
    impact_level = fields.Integer(string='Nivel de Impacto', compute='_compute_significance', store=True)
    significance = fields.Selection(
        SIGNIFICANCE_SELECTION, string='Significancia', compute='_compute_significance', store=True)
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        relation='sga_ideaa_matrix_line_action_rel',
        column1='line_id',
        column2='action_id',
        string='Medidas de control para implementar',
    )

    @api.depends('frequency', 'severity', 'scope')
    def _compute_significance(self):
        for each in self:
            level = compute_impact_level(each.frequency, each.severity, each.scope)
            each.impact_level = level
            each.significance = compute_significance(level)
