from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    department_id = fields.Many2one(
        'hr.department', 
        string='Departamento',
        check_company=True,   
    )
    process_id = fields.Many2one(
        'mgmt.process', 
        string='Proceso', 
        domain=lambda self: self._domain_process_id() ,
    )
    project_manager_id = fields.Many2one(
        'hr.employee',
        string='Jefe de proyecto',
        check_company=True,
    )
    start_date = fields.Date(string='Fecha de apertura')
    deadline_date = fields.Date(string='Fecha límite')
    
    def _domain_process_id(self):
        return [
            ('active', '=', True),
            '|',
            ('company_id', '=', False),
            ('company_id', '=', self.company_id),
        ]


class Task(models.Model):
    _inherit = 'project.task'

    risk_ids = fields.Many2many(
        'matrix.block.line', 
        relation='project_task_risk_rel',
        column1='task_id', 
        column2='risk_id',
        string='Riesgos', 
        domain= lambda self: self._domain_risk_ids()
    )
    opp_ids = fields.Many2many(
        'matrix.block.line', 
        relation='project_task_opp_rel',
        column1='task_id', column2='opp_id',
        string='Oportunidades', 
        domain=lambda self: self._domain_opp_ids(),
    )
    
    def _domain_opp_ids(self):
        return [
            ('type', '=', 'opportunity'),
            '|',
            ('company_id', '=', False),
            ('company_id', '=', self.company_id.id),
        ]
    
    def _domain_risk_ids(self):
        return [
            ('type', '=', 'risk'),
            '|',
            ('company_id', '=', False),
            ('company_id', '=', self.company_id.id),
        ]
