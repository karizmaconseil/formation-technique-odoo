# -*- coding: utf-8 -*-
from pprint import pprint

from odoo import models, fields, api


class OdooVersion(models.Model):
    _name = 'odoo.version'
    _description = "Odoo Version"

    name = fields.Char(string="Designation")
    current_version = fields.Boolean(string="Current version")
