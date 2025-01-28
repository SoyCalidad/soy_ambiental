from odoo import api, fields, models


class SGAAbstract(models.Model):
    _name = 'sga.abstract'
    _description = 'SGA Abstract'

    is_sga_context = fields.Boolean(string='SGA Context', default=False,
                                    help='Si se establece en True, ciertos campos se ocultarán en formularios e informes '
                                         'cuando se acceda a ellos a través del contexto SGA.')
