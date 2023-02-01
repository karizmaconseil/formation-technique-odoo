# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InstanceRequest(models.Model):
    _inherit = 'instance.request'

    cpu = fields.Char(string="CPU")


class NewInstanceRequest(models.Model):
    _name = 'new.instance.request'
    _inherit = 'instance.request'

    cpu = fields.Char(string="CPU")


class SecondInstanceRequest(models.Model):
    _name = 'second.instance.request'
    _inherits = {'instance.request': 'instance_id'}

    attachment_id = fields.Many2one(
        "instance.request",
        required=True,
        ondelete="cascade",
    )
