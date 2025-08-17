import logging
import requests
import json
import re
from urllib.parse import urlencode


from odoo import models, fields

_logger = logging.getLogger(__name__)


def sanitize_phone_number(phone_number):
    """
    Clean up the phone number to match the expected format.
    This removes any non-numeric characters and converts local numbers
    (e.g., starting with 0) to international format (e.g., 254...).
    """
    digits_only = re.sub(r'\D', '', phone_number)

    # Handle common cases for Kenyan numbers
    if digits_only.startswith('0') and len(digits_only) == 10:
        digits_only = '254' + digits_only[1:]
    elif digits_only.startswith('+'):
        digits_only = digits_only[1:]

    return digits_only


class SmsSms(models.Model):
    _inherit = 'sms.sms'

    error_message = fields.Char(string="Error Message")  
    sms_account_id = fields.Many2one('sms.account', string='SMS Account', required=True)


    

    def send(self, unlink_failed=False, unlink_sent=True, auto_commit=False, raise_exception=False):
        for sms in self:
            try:
                # Get the selected SMS account
                sms_account = sms.sms_account_id

                # Ensure that the SMS account exists and is active
                if not sms_account:
                    raise ValueError("SMS Account is not selected.")
                
                # Fetch the credentials from the selected SMS account
                url_base = sms_account.url
                apikey = sms_account.apikey
                partner_id = sms_account.partner_id
                shortcode = sms_account.shortcode

                if not (url_base and apikey and partner_id and shortcode):
                    raise ValueError("Missing SMS configuration in the selected account.")

                # Sanitize phone number
                sanitized_number = sanitize_phone_number(sms.number)

                # Compose full URL
                params = {
                    'apikey': apikey,
                    'partnerID': partner_id,
                    'shortcode': shortcode,
                    'mobile': sms.number,
                    'message': sms.body,
                }
                full_url = url_base + "?" + urlencode(params)

                _logger.debug("Sending SMS via Advanta API: %s", full_url)

                response = requests.get(full_url, timeout=10)
                response.raise_for_status()

                # Check if the response contains "Success" and the correct response-code
                response_data = response.json()
                if response_data.get("responses", [{}])[0].get("response-code") == 200:
                    _logger.info("SMS sent successfully to %s", sms.number)
                    sms.write({'state': 'sent'})
                else:
                    error_msg = response_data.get("responses", [{}])[0].get("response-description", "Unknown error") 
                    _logger.error("SMS delivery failed. Response: %s", response.text)
                    sms.write({'state': 'error', 'error_message': error_msg})
                    if raise_exception:
                        raise Exception(error_msg)
            except Exception as e:
                _logger.error("Error sending SMS to %s: %s", sms.number, e)
                sms.write({'state': 'error', 'error_message': str(e)})
                if raise_exception:
                    raise

        if auto_commit:
            self._cr.commit()

        

        return True

