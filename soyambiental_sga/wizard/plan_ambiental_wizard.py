from odoo import api, fields, models


class PlanAmbientalWizard(models.TransientModel):
    _name = 'plan.ambiental.wizard'
    _description = 'Asistente de Plan de saneamiento ambiental'

    plan_ambiental_ids = fields.Many2many('plan.ambiental', string='Planes de saneamiento ambiental')

    def action_export_pdf(self):
        return self.env.ref('plan_sanitation.plan_ambiental_report_action').report_action(
            self.plan_ambiental_ids.ids)
