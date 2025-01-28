from odoo import fields,models

class PlanR(models.TransientModel):
    _name = 'planr.ambiental'
    _description = 'Reporte de plan ambiental'
    plan_ambiental = fields.Many2many('plan.ambiental',string='Plan ambiental')

    def print_report(self):
        return self.env.ref('plan_sanitation.plan_ambiental_report_action').report_action(self.plan_ambiental) 