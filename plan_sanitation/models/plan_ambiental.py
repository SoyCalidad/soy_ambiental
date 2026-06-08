from odoo import fields, models, api
from odoo.exceptions import UserError

import logging 


_logger = logging.getLogger(__name__)


class NewPlanA(models.Model):
    _name = 'plan.ambiental'
    _description = 'Plan de saneamiento ambiental'
    codigo = fields.Char('Código')
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']

    name = fields.Text('Actividad')
    program = fields.Many2one('programa.ambiental', string='Programa')
    user_responsible = fields.Many2one(
        'res.users', string='Responsable interno')
    external_responsible = fields.Boolean('Responsable externo', default=True)
    responsible = fields.Many2one('res.partner', string='Responsable')
    frequency = fields.Many2one('mgmtsystem.frequency', string='Frecuencia')
    observations = fields.Text('Observaciones')
    month = fields.Selection([
        ('E', 'Enero'),
        ('F', 'Febrero'),
        ('Mar', 'Marzo'),
        ('A', 'Abril'),
        ('M', 'Mayo'),
        ('J', 'Junio'),
        ('Ju', 'Julio'),
        ('Ag', 'Agosto'),
        ('S', 'Septiembre'),
        ('O', 'Octubre'),
        ('N', 'Noviembre'),
        ('D', 'Diciembre'),
    ], string='Mes')
    date = fields.Date('Fecha')
    duration = fields.Text('Duración')
    initial_date = fields.Date('Fecha inicial')
    ambient = fields.Many2many('am.ambient', string='Ambientes')
    code = fields.Integer('Código')
    version = fields.Integer(string='Número de versión')
    date_validate = fields.Date('Fecha de validación')
    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'plan_ambiental_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'plan_ambiental_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'plan_ambiental_validation_id', string='Validación')
    process = fields.Text('Procedimiento')
    actions = fields.Many2many(
        'mgmtsystem.action', relation='relation_actions', string='Acciones')
    non_conformity = fields.Many2many(
        'mgmtsystem.nonconformity', relation='relation_non_conformity', string='No conformidades')
    target = fields.Many2many(
        'mgmtsystem.target', relation='relation_target', string='Objetivos')
    document = fields.Many2many(
        comodel_name='documents.document',  
        relation='relation_document', 
        string='Documentos',
        domain=[('type', '=', 'binary')],
    )
    change_request = fields.Many2many(
        'soycalidad.change_request', relation="relation_change_request", string='Solicitudes de cambio')
    target_counts = fields.Char(
        compute='_compute_target_counts', string='Cantidad de objetivos')
    nonconformities_counts = fields.Char(
        compute='_compute_nonconformities_counts', string='Cantidad de no conformidades')
    actions_counts = fields.Char(
        compute='_compute_actions_counts', string='Cantidad de acciones')
    document_counts = fields.Char(
        compute='_compute_document_counts', string='Cantidad de documentos')
    change_request_counts = fields.Char(
        compute='_compute_change_request_counts', string='Cantidad de solicitudes de cambio')
    area_responsible = fields.Many2one(
        'am.ambient', string='Responsable de Área')
    job = fields.Many2one('am.ambient', string='Puesto de trabajo')
    final_date = fields.Many2one('am.ambient', string='Última visita')
    company_id = fields.Many2one(
        string=u'Compañia',
        comodel_name='res.company', required=True,
        default=lambda self: self.env.user.company_id.id,
    )

    def send_email(self):
        self.ensure_one()
        template = self.env.ref(
            'plan_sanitation.email_plan_ambiental', raise_if_not_found=False)
        # self.env['mail.template'].browse(
        #     template.id).send_mail(self.id, force_send=True, notif_layout="mail.mail_notification_light",)
        if not template:
            raise UserError("La plantilla de correo no fue encontrada")

        lang = None
        if template.lang:
            lang = template._render_template(
                template.lang, self._name, self.ids[0])
        ctx = {
            'default_model': self._name,
            'default_res_id': self.ids[0],
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_light",
            'force_email': True,
            'model_description': self.with_context(lang=lang).name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_notify_employee(self):
        for each in self:
            self.env.cr.execute("""SELECT id FROM ir_model
                            WHERE model = %s""", (str(each._name),))
            info = self.env.cr.dictfetchall()
            if info:
                model_id = info[0]['id']
            else:
                raise UserError("No se encontro la información")
            #message = ""
            if each.user_responsible:
                self.env['mail.activity'].create({
                    'res_id': each.id,
                    'res_model_id': model_id,
                    'res_model': each._name,
                    'summary': 'Invitación a empleado',
                    'note': 'El empleado '+each.user_responsible.name+' queda cordialmente invitado a visualizar el plan ambiental '+each.name+' el '+each.date.strftime('%d/%m/%Y'),
                    'date_deadline': each.date,
                    'user_id': each.user_responsible.id,
                })
            # if message != "":
            #     each.message_post(
            #         body='Empleados que no recibieron notificación:<br></br>'+message)

    def send_process(self):
        self.write({'state': 'in_process'})

    def send_final(self):
        self.write({'state': 'final'})

    @api.depends('change_request')
    def _compute_change_request_counts(self):
        for each in self:
            each.change_request_counts = len(each.change_request)
        pass

    @api.depends('document')
    def _compute_document_counts(self):
        for each in self:
            each.document_counts = len(each.document)
        pass

    @api.depends('non_conformity')
    def _compute_nonconformities_counts(self):
        for each in self:
            each.nonconformities_counts = len(each.non_conformity)
        pass

    @api.depends('target')
    def _compute_target_counts(self):
        for each in self:
            each.target_counts = len(each.target)
        pass

    @api.depends('actions')
    def _compute_actions_counts(self):
        for each in self:
            each.actions_counts = len(each.actions)
        pass

    def openviews(self):
        type_action = self._context.get('type_action', '')
        action_rec = {}
        if type_action == 'target':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_auditplan_target').read()[0]
            domain = [('id', 'in', self.target.ids)]
            action_rec['domain'] = domain

        elif type_action == 'non_conformity':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_auditplan_nc').read()[0]
            domain = [('id', 'in', self.non_conformity.ids)]
            action_rec['domain'] = domain

        elif type_action == 'actions':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_auditplan_action').read()[0]
            domain = [('id', 'in', self.actions.ids)]
            action_rec['domain'] = domain

        elif type_action == 'document':
            action_rec = self.env.ref(
                'documents.document_action').read()[0]
            domain = [('id', 'in', self.document.ids)]
            action_rec['domain'] = domain

        elif type_action == 'change_request':
            action_rec = self.env.ref(
                'soycalidad_improve.improve_plan_action').read()[0]
            domain = [('id', 'in', self.change_request.ids)]
            action_rec['domain'] = domain

        return action_rec if action_rec else False


class Ambient(models.Model):
    _name = 'am.ambient'
    _description = 'Ambiente'
    name = fields.Char('Nombre de Ambiente')
    area_responsible = fields.Many2many(
        'hr.employee', string='Responsable de Área')
    job = fields.Many2many('hr.job', string='Puesto de trabajo')
    final_date = fields.Date('Última visita')


class Step(models.Model):
    _inherit = 'mgmtsystem.validation.step'
    plan_ambiental_elaboration_id = fields.Many2one(
        'plan.ambiental', string='padre Elaboración')
    plan_ambiental_review_id = fields.Many2one(
        'plan.ambiental', string='padre Revisión')
    plan_ambiental_validation_id = fields.Many2one(
        'plan.ambiental', string='padre Validación')
