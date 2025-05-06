from odoo import api, fields, models


class SGAIDEAAMatrixWizard(models.TransientModel):
    _name = 'sga.contigency_plan.wizard'
    _description = 'Asistente de Plan de contingencia'

    contigency_plan_ids = fields.Many2many('sst.contigency_plan', string='Planes de contingencia')

    def action_export_pdf(self):
        return self.env.ref('soyseguridad_contigency_plan.action_report_sst_contigency_plan').report_action(
            self.contigency_plan_ids.ids)
