from odoo import models, fields

class SmsAccount(models.Model):
    _name = 'sms.account'
    _description = 'SMS Account'

    name = fields.Char(string='Account Name', required=True)
    partner_id = fields.Char(string='Partner ID', required=True)
    apikey = fields.Char(string='API Key', required=True)
    shortcode = fields.Char(string='Shortcode', required=True)
    url = fields.Char(string='API URL', required=True)
    active = fields.Boolean(default=True)
