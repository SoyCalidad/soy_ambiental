from odoo import api, fields, models


class SGAIDEAAMatrixWizard(models.TransientModel):
    _name = 'sga.ideaa_matrix.wizard'
    _description = 'Asistente de Matriz de identificación de aspectos ambientales'

    ideaa_matrix_id = fields.Many2one('sga.ideaa_matrix', string='Matriz de identificación de aspectos ambientales')

    def action_export_xlsx(self):
        return self.env.ref('soyambiental_risk.ideaa_matrix_report_xlsx_action').report_action(self.ideaa_matrix_id.id)
