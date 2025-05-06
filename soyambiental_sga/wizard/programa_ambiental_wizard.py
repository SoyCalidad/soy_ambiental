from odoo import api, fields, models


class ProgramaAmbientalWizard(models.TransientModel):
    _name = 'programa.ambiental.wizard'
    _description = 'Asistente de Programa de saneamiento ambiental'

    programa_ambiental_ids = fields.Many2many('programa.ambiental', string='Programas de saneamiento ambiental')

    def action_export_pdf(self):
        return self.env.ref('plan_sanitation.programa_ambiental_action_report').report_action(
            self.programa_ambiental_ids.ids)
