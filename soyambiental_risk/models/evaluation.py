from odoo import api, fields, models
from odoo.exceptions import UserError


class MatrixEvaluationItemCriterio(models.Model):
    _name = 'sga.matrix.evaluation.item.criterio'
    _description = 'Criterios'

    name = fields.Char(string='Criterio')
    item_value_id = fields.Many2one('sga.matrix.evaluation.item.value', string='Valor')
    item_id = fields.Many2one('sga.matrix.evaluation.item', string='Item')


class MatrixEvaluationItemValue(models.Model):
    _name = 'sga.matrix.evaluation.item.value'
    _description = 'Valores'

    name = fields.Char(string='Valor')
    value = fields.Char(string='Valor numérico')
    description = fields.Text(string='Descripción')
    item_id = fields.Many2one('sga.matrix.evaluation.item', string='Item')


class MatrixEvaluationItem(models.Model):
    _name = 'sga.matrix.evaluation.item'
    _description = 'Item de evaluación'

    name = fields.Char(string='Nombre')
    values_ids = fields.One2many('sga.matrix.evaluation.item.value', 'item_id', string='Valores')
    has_criterios = fields.Boolean(string='¿Tiene criterios?')
    criterio_ids = fields.One2many('sga.matrix.evaluation.item.criterio', 'item_id', string='Criterios')
    evaluation_id = fields.Many2one('sga.matrix.evaluation', string='Evaluación')


class MatrixEvaluation(models.Model):
    _name = 'sga.matrix.evaluation'
    _description = 'Evaluación'

    name = fields.Char(string='Nombre')
    item_ids = fields.One2many('sga.matrix.evaluation.item', 'evaluation_id', string='Factores')
