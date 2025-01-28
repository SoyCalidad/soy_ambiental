from odoo import http
from odoo.http import request


class OnPlanController(http.Controller):

    @http.route('/plan_ambiental/principal', auth='user', type='json')
    def plan_sanidad_vista(self):

        company = request.env.company

        return {
            'html': request.env.ref('plan_sanitation.plan_sanidad_template').render({
                'company': company,
                'state': company.get_and_update_sanidad_state()
            })
        }
