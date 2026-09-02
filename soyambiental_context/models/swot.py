from odoo import models, fields, _, api 

class SWOT(models.Model):
    _inherit = "mgmtsystem.context.swot"
    
    identifier = fields.Selection(
        selection=[
            ('enviromental', 'Ambiental'),
        ],
        string="Soy Ambiental",
    )
    
    
class SWOTItem(models.Model):
    _inherit = 'mgmtsystem.context.swot.item'
    
    
    environmental_condition = fields.Selection(
        selection=[
            ('climate_change', 'Cambio climático'),
            ('biodiversity', 'Biodiversidad'),
            ('ecosystem_health', 'Salud de los ecosistemas'),
            ('natural_resources', 'Disponibilidad de recursos naturales'),
            ('pollution_levels', 'Niveles de contaminación'),
            ('air_quality', 'Calidad del aire'),
            ('water_quality', 'Calidad del agua'),
            ('land_use', 'Uso del suelo'),
            ('other_environmental_condition', 'Otra condición ambiental'),
            ('not_applicable', 'No aplica'),
        ],
        string='Condición ambiental relacionada',
    )