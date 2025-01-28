from odoo import models,fields

class ProgramaR(models.TransientModel):
    _name = 'programar.ambiental'
    _description = 'Reporte de programa ambiental'
    programa_ambiental = fields.Many2many('programa.ambiental',string='Programa ambiental')

    def print_report(self):
        return self.env.ref('plan_sanitation.programa_ambiental_action_report').report_action(self.programa_ambiental) 
