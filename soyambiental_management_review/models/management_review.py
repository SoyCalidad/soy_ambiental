from odoo import api, fields, models, _


XMLID_ACTION_IDEAA_MATRIX = "soyambiental_risk.sga_ideaa_matrix_action"
XMLID_ACTION_LEGAL_PLAN = "mgmtsystem_legal.legal_plan_action"
XMLID_ACTION_AUDIT_PLAN = "mgmtsystem_audit.audit_plan_action"

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
    
    sa_significant_aspects = fields.Html(string="B.3 Aspectos ambientales significativos")
    sa_significant_aspects_interpretation = fields.Html(string="Interpretación de Aspectos ambientales significativos")
    
    sa_risk_opp = fields.Html(string="Riesgos y oportunidades ambientales")
    sa_risk_opp_interpretation = fields.Html(string="Interpretación Riesgos y oportunidades ambientales")
    
    sa_assessment_compliance_obligations = fields.Html(string="Evaluación del cumplimiento de obligaciones")
    sa_aco_interpretation = fields.Html(string="Interpretacion Evaluación del cumplimiento de obligaciones")
    
    sa_communication = fields.Html(string="Comunicaciones / quejas / consultas")
    sa_communication_interpretation = fields.Html(string="Interpretación Comunicaciones / quejas / consultas")
    
    
    def generate_sa_significant_aspects_html(self):
        if self.is_last:
            matrix_ids = self.env['sga.ideaa_matrix'].search([], order="create_date desc", limit=1)
        else:
            matrix_ids = self.env['sga.ideaa_matrix'].search([
                ('date_validate', '>=', self.date_ini), 
                ('date_validate', '<=', self.date_fin)
            ])       
        data_tmp = "<table class='table table-bordered'>"
        data_tmp += "<tr><td><strong>ETAPA</strong></td><td><strong>ACTIVIDAD</strong></td><td><strong>TAREA</strong></td><td><strong>PUESTO DE TRABAJO</strong><td><strong>ASPECTOS</strong></td><td><strong>IMPACTOS</strong></td><td><strong>NIVEL DE RIESGO PURO</strong></td><td><strong>NIVEL DE RIESGO RESIDUAL</strong></td></tr>" 
        action = self.env.ref(XMLID_ACTION_IDEAA_MATRIX, raise_if_not_found=False)
        for data in matrix_ids:
            
            for control in data.process_control_ids:
                link = (
                    '<a href="/odoo/action-%s/%s" '
                    'data-oe-id="%s" '
                    'data-oe-model="sga.ideaa_matrix">%s</a>'
                ) % (
                    action.id if action else 0,
                    data.id,
                    data.id,
                    control.stage_id.display_name or '',
                )
                data_tmp += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                link, control.activity_id.display_name or '', control.task_id.display_name or '', ", ".join(control.job_ids.mapped('display_name')), ", ".join(control.aspect_ids.mapped('display_name')), ", ".join(control.impact_ids.mapped('display_name')), control.level, control.control_level,)
            
        data_tmp = data_tmp + "</table>"
        return data_tmp
    
    
    def generate_legal_plan_html(self):
        if self.is_last:
            legal_requirements_ids = self.env['legal.plan'].search([], order='create_date desc', limit=1)
        else:
            legal_requirements_ids = self.env['legal.plan'].search(
                [('date_validate', '>=', self.date_ini), ('date_validate', '<=', self.date_fin)], order='date_validate asc')
        data_tmp = "<table class='table table-bordered'>"
        data_tmp += "<tr><td><strong>Nombre</strong></td><td><strong>Fecha validación</strong></td><td><strong>Estado</strong></td></tr>"
        action = self.env.ref(XMLID_ACTION_LEGAL_PLAN, raise_if_not_found=False)
        for data in legal_requirements_ids:
            link = (
                '<a href="/odoo/action-%s/%s" '
                'data-oe-id="%s" '
                'data-oe-model="legal.plan">%s</a>'
            ) % (
                action.id if action else 0,
                data.id,
                data.id,
                data.name or 'Sin nombre',
            )
            data_tmp += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                link, data.date_validate, data.state)
            data_tmp += "<tr><td><strong>Requisito</strong></td><td><strong>Fecha de publicación</strong></td><td><strong>Responsable</strong></td></tr>"
            for line in data.line_ids:
                data_tmp += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    line.legal_id.name, line.date_release, line.user_id.name)
        data_tmp = data_tmp + "</table>"
        return data_tmp
    
    def generate_complaint_html(self):
        if self.is_last:
            complaint_ids = self.env['complaint.complaint'].search([], order='create_date desc', limit=1)
        else:
            complaint_ids = self.env['complaint.complaint'].search(
                [], order='create_date asc')
        data_tmp = "<table class='table table-bordered'>"
        data_tmp += "<tr><td><strong>Nombre</strong></td><td><strong>Motivo</strong></td><td><strong>Categoria</strong></td><td><strong>Estado</strong></td></tr>"
        action = self.env.ref(XMLID_ACTION_LEGAL_PLAN, raise_if_not_found=False)
        state_dict = dict(self.env['complaint.complaint']._fields['state'].selection)
        for data in complaint_ids:
            link = (
                '<a href="/odoo/action-%s/%s" '
                'data-oe-id="%s" '
                'data-oe-model="complaint.complaint">%s</a>'
            ) % (
                action.id if action else 0,
                data.id,
                data.id,
                data.name or 'Sin nombre',
            )
            data_tmp += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                link, ", ".join(data.reason_ids.mapped('name')), data.categ_id.display_name or '', state_dict.get(data.state, '')) 
        data_tmp = data_tmp + "</table>"
        return data_tmp
    
    def generate_audit_plan_html(self):
        """Programa de auditoria"""
        if self.is_last:
            audit_plans = self.env['audit.plan'].search([], order='create_date desc', limit=1)
        else:
            audit_plans = self.env['audit.plan'].search(
                [
                    ('date_validate', '>=', self.date_ini), 
                                    ('date_validate', '<=', self.date_fin)], order='create_date asc')
        data_tmp = "<table class='table table-bordered'>"
        data_tmp += "<tr><td><strong>Nombre del programa</strong></td><td><strong>Actividad</strong></td><td><strong>Tipo</strong></td><td><strong>Fecha de inicio</strong></td></tr>"
        action = self.env.ref(XMLID_ACTION_AUDIT_PLAN, raise_if_not_found=False)
        audit_type_dict = dict(self.env['audit.audit']._fields['type'].selection)
        for data in audit_plans:
            link = (
                '<a href="/odoo/action-%s/%s" '
                'data-oe-id="%s" '
                'data-oe-model="audit.plan">%s</a>'
            ) % (
                action.id if action else 0,
                data.id,
                data.id,
                data.name or 'Sin nombre',
            )
            for audit in data.audit_ids:
                data_tmp += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    link, audit.name, audit_type_dict.get(audit.type, ''), audit.date_init or '') 
        data_tmp = data_tmp + "</table>"
        return data_tmp

    def update_data(self):
        super().update_data()
        
        if self.type_review == 'iso14001':
            self.generate_record_meeting_ids()
            self.foda = self.generate_foda()
            self.generate_stakeholders()
            self.sa_significant_aspects = self.generate_sa_significant_aspects_html()
            self.risk = self.generate_risk()
            self.target = self.generate_target()
            self.nonconformity_action = self.generate_nonconformity_action()
            self.measurement_html = self.generate_target()
            self.legal_requirements = self.generate_legal_plan_html()
            self.audit = self.generate_audit_plan_html()
            self.sa_communication = self.generate_complaint_html()

                
                
                