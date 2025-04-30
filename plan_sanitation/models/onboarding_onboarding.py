from odoo import api, models


class Onboarding(models.Model):
    _inherit = 'onboarding.onboarding'

    # Sale Quotation Onboarding
    @api.model
    def action_close_plan_sanitation(self):
        self.action_close_panel('plan_sanitation.onboarding_onboarding_sale_quotation')