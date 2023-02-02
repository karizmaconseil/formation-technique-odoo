# -*- coding: utf-8 -*-
from pprint import pprint

from odoo import models, fields, api


class InstanceRequestLine(models.Model):
    _name = 'instance.request.line'
    _description = "Instance request line"

    name = fields.Char(string="Designation")
    instance_id = fields.Many2one('instance.request', string="Instance request")
    odoo_version_id = fields.Many2one(related='instance_id.odoo_version_id')

