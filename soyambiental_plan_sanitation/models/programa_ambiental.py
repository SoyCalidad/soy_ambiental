from odoo import fields, models, api


class NewPlanP(models.Model):
    _inherit = 'programa.ambiental'

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
        comodel_name='programa.ambiental', string='Padre', copy=False,
    )
    old_versions = fields.One2many(
        comodel_name='programa.ambiental', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False},
    )
