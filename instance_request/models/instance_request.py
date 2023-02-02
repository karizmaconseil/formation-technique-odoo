# -*- coding: utf-8 -*-
from pprint import pprint

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class InstanceRequest(models.Model):
    _name = 'instance.request'
    _description = "Instance request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Designation")
    limit_date = fields.Date(string="Date limite de traitement", tracking=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("in_progress", "In progress"),
            ("done", "Done"),
        ],
        default="draft",
    )
    color = fields.Selection(
        [('red', "Red"), ('green', "Green"), ('yellow', "Yellow")], default='red', tracking=True
    )
    cpu = fields.Integer(string="CPU")
    ram = fields.Float(string="RAM")

    odoo_version_id = fields.Many2one('odoo.version', string="Version odoo")
    odoo_version_ids = fields.Many2many('odoo.version', string="Versions odoo")
    requests_line_ids = fields.One2many('instance.request.line', 'instance_id', string="Lines")

    nb_lines = fields.Integer(string="Nb lines", compute='_compute_nb_lines', store=1)

    @api.depends('requests_line_ids')
    def _compute_nb_lines(self):
        for record in self:
            record.nb_lines = len(record.requests_line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        print("======> vals_list")
        pprint(vals_list)
        for val in vals_list:
            print("===>", val)
            val['cpu'] = 2
            print("===>", val)
        records = super().create(vals_list)
        print("======> records", records)
        for rec in records:
            print("=====> RAM before", rec.ram)
            rec.ram = 16
            print("=====> RAM after", rec.ram)

        return records

    def write(self, vals):
        result = super().write(vals)
        return result

    def unlink(self):
        if self.state == 'done':
            raise UserError("You can't delete a record in state done")
        result = super().unlink()
        return result

    @api.onchange('color', 'name', 'state')
    def recal_limit_date(self):
        for record in self:
            if record.color == 'red':
                record.limit_date = False
            else:
                record.limit_date = fields.Date.today()

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_submit(self):
        for record in self:
            get_if_submit = self.env.context.get('get_if_submit', False)
            print("===============>", get_if_submit)
            record.state = 'submitted'

    def action_progress(self):
        for record in self:
            record.state = 'in_progress'
            user_group = self.env.ref('instance_request.group_instance_request_user')
            users = user_group.users
            user_connected = self.env.user
            print("user_connected ===>", user_connected)
            has_user_group = user_connected.has_group('instance_request.group_instance_request_user')
            print("has_user_group ===>", has_user_group)
            for user in users:
                print("=======> name", user.name)
            print("=======>", user_group)
            model_access = user_group.model_access
            print("================== model_access")
            for access in model_access:
                print("====>", access.name, access.perm_create, access.perm_write, access.perm_read, access.perm_unlink)

            resp_group = self.env.ref('instance_request.group_instance_request_resp')
            users = resp_group.users
            for user in users:
                record.activity_schedule(
                    'instance_request.create_instance_activity', user_id=user.id, date_deadline=record.limit_date
                )

    def action_done(self):
        for record in self:
            if not record.limit_date:
                raise ValidationError("You cant done a request without limit date")
            record.state = 'done'
            record.activity_feedback(['instance_request.create_instance_activity'])
            template = self.env.ref('instance_request.instance_request_creation')
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})
