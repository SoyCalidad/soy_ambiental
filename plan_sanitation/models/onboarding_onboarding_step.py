from odoo import _, api, Command, models
from odoo.tools import file_open


class OnboardingStep(models.Model):
    _inherit = 'onboarding.onboarding.step'

    @api.model
    def action_open_step_programa_ambiental(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Cree un programa de saneamiento ambiental'),
            'res_model': 'programa.ambiental',
            'view_mode': 'form',
            'views': [(self.env.ref('plan_sanitation.programa_ambiental_view_form').id, 'form')],
            'target': 'new',
        }
        return action

    @api.model
    def action_open_step_plan_ambiental(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Cree un plan de saneamiento ambiental'),
            'res_model': 'plan.ambiental',
            'view_mode': 'form',
            'views': [(self.env.ref('plan_sanitation.plan_ambiental_view_form').id, 'form')],
            'target': 'new',
        }
        return action
