from odoo import fields, models, api


class NewPlanA(models.Model):
    _inherit = 'plan.ambiental'

    state = fields.Selection(
        string='Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('in_process', 'En proceso'),
            ('final', 'Finalizado'),
            ('cancel', 'Obsoleto'),
        ],
        default='elaborate',
        copy=False,
    )
    parent_edition = fields.Many2one(
        comodel_name='plan.ambiental', string='Padre', copy=False,
    )
    old_versions = fields.One2many(
        comodel_name='plan.ambiental', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False},
    )
