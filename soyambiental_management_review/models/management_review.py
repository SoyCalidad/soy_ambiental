from odoo import api, fields, models, _

class ManagementReview(models.Model):
    _inherit = 'management.review'


    c4_matriz = fields.Text(string="Matriz")
    c4_interpretation = fields.Text(string="Interpretación")
    
    # c.5 saneamiento ambiental
    c5_plan = fields.Text(string="Plan")
    c5_interpretation = fields.Text(string="Interpretación")
    
    
    # c.6 plan de contingencia
    c6_plan = fields.Text(string="Plan")
    c6_interpretation = fields.Text(string="Interpretación")