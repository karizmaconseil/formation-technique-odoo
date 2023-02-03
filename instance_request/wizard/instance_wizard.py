# -*- coding: utf-8 -*-
from pprint import pprint

from odoo import models, fields, api


class InstanceWizard(models.TransientModel):
    _name = 'instance.wizard'
    _description = 'Instance Wizard'

    odoo_version_id = fields.Many2one('odoo.version', string="Odoo Version")
    partner_ids = fields.Many2many('res.partner', string="Partners")

    def apply_odoo_version(self):
        for partner in self.partner_ids:
            partner.odoo_version_id = self.odoo_version_id.id
