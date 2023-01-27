# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InstanceRequest(models.Model):
    _name = 'instance.request'
    _description = "Instance request"

    name = fields.Char(string="Designation")
    limit_date = fields.Date(string="Date limite de traitement")
