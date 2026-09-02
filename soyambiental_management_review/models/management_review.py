from odoo import api, fields, models, _

class ManagementReview(models.Model):
    _inherit = 'management.review'


    type_review = fields.Selection(
        selection_add=[
            ('iso14001', '14001'),
        ],
    )
    
    sa_c4_matriz = fields.Text(string="Matriz")
    sa_c4_interpretation = fields.Text(string="Interpretación")
    
    # c.5 saneamiento ambiental
    sa_c5_plan = fields.Text(string="Plan")
    sa_c5_interpretation = fields.Text(string="Interpretación")
    
    
    # c.6 plan de contingencia
    sa_c6_plan = fields.Text(string="Plan")
    sa_c6_interpretation = fields.Text(string="Interpretación")
    
    
    #new
    
    sa_significant_aspects = fields.Html(string="Aspectos ambientales significativos")
    sa_significant_aspects_interpretation = fields.Html(string="Interpretación de Aspectos ambientales significativos")
    
    sa_risk_opp = fields.Html(string="Riesgos y oportunidades ambientales")
    sa_risk_opp_interpretation = fields.Html(string="Interpretación Riesgos y oportunidades ambientales")
    
    sa_assessment_compliance_obligations = fields.Html(string="Evaluación del cumplimiento de obligaciones")
    sa_aco_interpretation = fields.Html(string="Interpretacion Evaluación del cumplimiento de obligaciones")
    
    sa_communication = fields.Html(string="Comunicaciones / quejas / consultas")
    sa_communication_interpretation = fields.Html(string="Interpretación Comunicaciones / quejas / consultas")
    