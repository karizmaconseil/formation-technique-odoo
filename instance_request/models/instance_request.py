# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
            record.state = 'done'
            record.activity_feedback(['instance_request.create_instance_activity'])
            template = self.env.ref('instance_request.instance_request_creation')
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})
