# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InstanceRequest(models.Model):
    _name = 'instance.request'
    _description = "Instance request"

    name = fields.Char(string="Designation")
    limit_date = fields.Date(string="Date limite de traitement")
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
        [('red', "Red"), ('green', "Green"), ('yellow', "Yellow")], default='red'
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

    def action_done(self):
        for record in self:
            record.state = 'done'
