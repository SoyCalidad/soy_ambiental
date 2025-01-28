from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    department_id = fields.Many2one('hr.department', string='Departamento')
    process_id = fields.Many2one('mgmt.process', string='Proceso', domain=[('active', '=', True)])
    project_manager_id = fields.Many2one('hr.employee', string='Jefe de proyecto')
    start_date = fields.Date(string='Fecha de apertura')
    deadline_date = fields.Date(string='Fecha límite')


class Task(models.Model):
    _inherit = 'project.task'

    risk_ids = fields.Many2many('matrix.block.line', relation='project_task_risk_rel',
                                column1='task_id', column2='risk_id',
                                string='Riesgos', domain=[('type', '=', 'risk')])
    opp_ids = fields.Many2many('matrix.block.line', relation='project_task_opp_rel',
                               column1='task_id', column2='opp_id',
                               string='Oportunidades', domain=[('type', '=', 'opportunity')])
