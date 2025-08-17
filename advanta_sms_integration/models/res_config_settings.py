from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    smske_partnerID = fields.Char(related='company_id.smske_partnerID', readonly=False)
    smske_apikey = fields.Char(related='company_id.smske_apikey', readonly=False)
    smske_shortcode = fields.Char(related='company_id.smske_shortcode', readonly=False)
    smske_url = fields.Char(related='company_id.smske_url', readonly=False)