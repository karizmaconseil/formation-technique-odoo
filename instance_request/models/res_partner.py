# -*- coding: utf-8 -*-
from pprint import pprint

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    odoo_version_id = fields.Many2one('odoo.version', string="Odoo Version")
