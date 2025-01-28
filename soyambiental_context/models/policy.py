from odoo import api, fields, models


class Policy(models.Model):
    _inherit = 'mgmtsystem.context.policy'

    sga_organization_context = fields.Text(string='Contexto de la organización')
    sga_direction_help = fields.Text(string='Apoyo para la dirección')
    sga_env_protection_commitment = fields.Text(string='Compromiso protección medio ambiente')
    sga_legal_req = fields.Text(string='Requisitos Legales')
    sga_standard_commitment = fields.Text(string='Compromiso para los requisitos de la norma')
    sga_continuous_improvement = fields.Text(string='Mejora Continua')
    sga_env_goals = fields.Text(string='Objetivos ambientales')
    sga_communication = fields.Text(string='Comunicación')

    @api.onchange('template_')
    def _onchange_template_(self):
        super()._onchange_template_()
        self.name = self.template_.name
        self.sga_organization_context = self.template_.sga_organization_context
        self.sga_direction_help = self.template_.sga_direction_help
        self.sga_env_protection_commitment = self.template_.sga_env_protection_commitment
        self.sga_legal_req = self.template_.sga_legal_req
        self.sga_standard_commitment = self.template_.sga_standard_commitment
        self.sga_continuous_improvement = self.template_.sga_continuous_improvement
        self.sga_env_goals = self.template_.sga_env_goals
        self.sga_communication = self.template_.sga_communication


class PolicyTemplate(models.Model):
    _inherit = 'mgmtsystem.context.policy.template'

    sga_organization_context = fields.Text(string='Contexto de la organización')
    sga_direction_help = fields.Text(string='Apoyo para la dirección')
    sga_env_protection_commitment = fields.Text(string='Compromiso protección medio ambiente')
    sga_legal_req = fields.Text(string='Requisitos Legales')
    sga_standard_commitment = fields.Text(string='Compromiso para los requisitos de la norma')
    sga_continuous_improvement = fields.Text(string='Mejora Continua')
    sga_env_goals = fields.Text(string='Objetivos ambientales')
    sga_communication = fields.Text(string='Comunicación')
