from odoo import models,fields,api

class Principal(models.Model):
    _inherit = 'res.company'

    plan_sanidad_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')
    plan_ambiental_p = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="Principal de plan ambiental", default='not_done')
    programa_ambiental_p = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="Principal de programa ambiental", default='not_done')

    @api.model
    def action_open_plan_ambiental(self, action_ref=None):
        if not action_ref:
            action_ref = 'plan_sanitation.action_principal_plan_ambiental'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_programa_ambiental(self, action_ref=None):
        if not action_ref:
            action_ref = 'plan_sanitation.action_principal_programa_ambiental'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_plan_sanidad(self):
        """ Mark the invoice onboarding panel as closed. """
        pass
        #self.env.company.plan_sanidad_state = 'closed'

    def get_and_update_sanidad_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'plan_ambiental_p',
            'programa_ambiental_p'
        ]
        return self.get_and_update_onbarding_state('plan_sanidad_state', steps)

    

class PlanP(models.Model):
    _inherit= 'plan.ambiental'
    _description = 'Vista de plan ambiental'

    @api.model
    def action_open_plan_ambiental(self, action_ref=None):
        if not action_ref:
            action_ref = 'plan_sanitation.action_principal_plan_ambiental'
        return self.env.ref(action_ref).read()[0]

    def action_save_plan_ambiental(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'plan_ambiental_p')

class ProgramaP(models.Model):
    _inherit= 'programa.ambiental'
    _description = 'Vista de programa ambiental'

    @api.model
    def action_open_programa_ambiental(self, action_ref=None):
        if not action_ref:
            action_ref = 'plan_sanitation.action_principal_plan_ambiental'
        return self.env.ref(action_ref).read()[0]

    def action_save_programa_ambiental(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'programa_ambiental_p')





