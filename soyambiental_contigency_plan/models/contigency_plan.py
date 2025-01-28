from odoo import api, fields, models


class ContigencyPlan(models.Model):
    _name = 'sst.contigency_plan'
    _inherit = ['sst.contigency_plan', 'sga.abstract']
