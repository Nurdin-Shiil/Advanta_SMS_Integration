
import re
from odoo import api, fields, models
from odoo.exceptions import UserError


class SendSMS(models.TransientModel):
    _inherit = 'sms.composer'
    
    sms_account_id = fields.Many2one('sms.account', string='SMS Account')


    @api.depends('res_model', 'number_field_name')
    def _compute_recipient_single(self):
        """
        This computed method pulls the correct phone number and recipient
        details based on the model and record being messaged.
        """
        for composer in self:
            records = composer._get_records()

            # Basic safety checks
            if not records or not hasattr(records, '_sms_get_recipients_info'):
                composer.recipient_single_description = False
                composer.recipient_single_number = ''
                composer.recipient_single_number_itf = ''
                continue

            records.ensure_one()  # We're only dealing with one recipient here
            res = records._sms_get_recipients_info(force_field='mobile', partner_fallback=False)

            # Show recipient name in the wizard
            composer.recipient_single_description = res[records.id]['partner'].name or records.display_name

            # Extract phone number and assign it
            phone_no = res[records.id]['number'] or ''
            composer.recipient_single_number = phone_no
            composer.recipient_single_number_itf = phone_no
            composer.number_field_name = res[records.id]['field_store']

    def action_send_sms(self):
        """
        This method is triggered when the user clicks "Send" in the SMS wizard.
        It creates an `sms.sms` record and calls the `.send()` method
        that we extended to send via Advanta.
        """
        for wizard in self:
            if not wizard.recipient_single_number:
                raise UserError("Recipient phone number is missing.")

            # Create a new SMS record
            sms = self.env['sms.sms'].create({
                'number': wizard.recipient_single_number,
                'body': wizard.body or '',
                
                'state': 'outgoing',
            })

            # Send the message using our override
            sms.send()

            # If it failed, raise error in wizard
            if sms.state == 'error':
                raise UserError(f"SMS sending failed: {sms.error_message or 'Unknown error'}")
            
    def _prepare_mass_sms_values(self, records):
        result = super()._prepare_mass_sms_values(records)
        if self.composition_mode == 'mass':
            for record in records:
                sms_vals = result[record.id]
                sms_vals.update({
                    'sms_account_id': self.sms_account_id.id,
                })
        return result
    

