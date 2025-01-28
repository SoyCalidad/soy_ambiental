from odoo import fields, models, api


class NewPlanP(models.Model):
    _name = 'programa.ambiental'
    _description = 'Programa ambiental'
    _inherit = ['mgmtsystem.validation.mail',
                'model.origin.abstract', 'mgmtsystem.code']

    code = fields.Char('Código')
    name = fields.Char('Nombre')
    plans = fields.Many2many('plan.ambiental', string='Planes')
    actions = fields.Many2many('mgmtsystem.action', string='Acciones')
    non_conformities = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades')
    target = fields.Many2many('mgmtsystem.target', string='Objetivos')
    documents = fields.Many2many(
        'dms.file', relation='relation_documents', string='Documentos')
    change_requests = fields.Many2many(
        'soycalidad.change_request', relation="relation_change_requests", string='Solicitudes de cambio')
    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'programa_ambiental_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'programa_ambiental_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'programa_ambiental_validation_id', string='Validación')
    responsible = fields.Many2many('res.users', string='Responsable')
    target_counts = fields.Char(
        compute='_compute_target_counts', string='Cantidad de objetivos')
    nonconformities_counts = fields.Char(
        compute='_compute_nonconformities_counts', string='Cantidad de no conformidades')
    actions_counts = fields.Char(
        compute='_compute_actions_counts', string='Cantidad de acciones')
    documents_counts = fields.Char(
        compute='_compute_documents_counts', string='Cantidad de documentos')
    change_requests_counts = fields.Char(
        compute='_compute_change_requests_counts', string='Cantidad de solicitudes de cambio')
    plans_counts = fields.Char(
        compute='_compute_plans_counts', string='Cantidad de planes')

    @api.depends('plans')
    def _compute_plans_counts(self):
        for each in self:
            each.plans_counts = len(each.plans)
        pass

    @api.depends('change_requests')
    def _compute_change_requests_counts(self):
        for each in self:
            each.change_requests_counts = len(each.change_requests)
        pass

    @api.depends('documents')
    def _compute_documents_counts(self):
        for each in self:
            each.documents_counts = len(each.documents)
        pass

    @api.depends('non_conformities')
    def _compute_nonconformities_counts(self):
        for each in self:
            each.nonconformities_counts = len(each.non_conformities)
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

        elif type_action == 'non_conformities':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_auditplan_nc').read()[0]
            domain = [('id', 'in', self.non_conformities.ids)]
            action_rec['domain'] = domain

        elif type_action == 'actions':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_auditplan_action').read()[0]
            domain = [('id', 'in', self.actions.ids)]
            action_rec['domain'] = domain

        elif type_action == 'documents':
            action_rec = self.env.ref(
                'dms.action_dms_file').read()[0]
            domain = [('id', 'in', self.documents.ids)]
            action_rec['domain'] = domain

        elif type_action == 'change_requests':
            action_rec = self.env.ref(
                'soycalidad_improve.improve_plan_action').read()[0]
            domain = [('id', 'in', self.change_requests.ids)]
            action_rec['domain'] = domain

        elif type_action == 'plans':
            action_rec = self.env.ref(
                'plan_sanitation.plan_ambiental_action').read()[0]
            domain = [('id', 'in', self.plans.ids)]
            action_rec['domain'] = domain

        return action_rec if action_rec else False

    def button_new_version(self):
        self.ensure_one()
        old_edition = self._copy_edition()
        revno = self.version
        self.write({
            'version': revno + 1,
            'state': 'elaborate',
            'name': self.name
        })
        child_fields = ['targets', 'non_conformities',
                        'actions', 'documents', 'change_requests', 'plans']

        for field in child_fields:
            if hasattr(self, field):
                lines = getattr(self, field)
                old_childs = self.clone_childs(lines)
                old_edition.write({field: [(6, 0, old_childs)]})


class Step(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    programa_ambiental_elaboration_id = fields.Many2one(
        'programa.ambiental', string='padre Elaboración')
    programa_ambiental_review_id = fields.Many2one(
        'programa.ambiental', string='padre Revisión')
    programa_ambiental_validation_id = fields.Many2one(
        'programa.ambiental', string='padre Validación')
