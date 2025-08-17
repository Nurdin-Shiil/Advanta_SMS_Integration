# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    smske_partnerID = fields.Char('Partner ID', groups="base.group_erp_manager",help='partnerID')
    smske_apikey = fields.Char('Api Key', groups="base.group_erp_manager", help='apikey')
    smske_shortcode = fields.Char('Shortcode', groups="base.group_erp_manager", help='shortcode')
    smske_url = fields.Char('API URL', groups="base.group_erp_manager")

