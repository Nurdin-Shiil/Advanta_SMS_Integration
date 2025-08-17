from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)



class Mailing(models.Model):
    _inherit = 'mailing.mailing'

    sms_account_id = fields.Many2one('sms.account', string='SMS Account')
    
    def action_test(self):
        res = super().action_test()
        res['context'] = dict(res.get('context', {}), default_sms_account_id=self.sms_account_id.id)
        return res
    
    def _send_sms_get_composer_values(self, res_ids):
        return {
            # content
            'body': self.body_plaintext,
            'template_id': self.sms_template_id.id,
            'res_model': self.mailing_model_real,
            'res_ids': repr(res_ids),
            'sms_account_id': self.sms_account_id.id,
            # options
            'composition_mode': 'mass',
            'mailing_id': self.id,
            'mass_keep_log': self.keep_archives,
            'mass_force_send': self.sms_force_send,
            'mass_sms_allow_unsubscribe': self.sms_allow_unsubscribe,
        }
        

class MailingSmsTest(models.TransientModel):
    _inherit = 'mailing.sms.test'
    
    sms_account_id = fields.Many2one('sms.account', string='SMS Account')
    
    def action_send_sms(self):
        self.ensure_one()
        numbers = [number.strip() for number in self.numbers.splitlines()]
        sanitized_numbers = [self.env.user._phone_format(number=number) for number in numbers]
        invalid_numbers = [number for sanitized, number in zip(sanitized_numbers, numbers) if not sanitized]
        sms_account = self.sms_account_id.id

        record = self.env[self.mailing_id.mailing_model_real].search([], limit=1)
        body = self.mailing_id.body_plaintext
        if record:
            # Returns a proper error if there is a syntax error with qweb
            body = self.env['mail.render.mixin']._render_template(body, self.mailing_id.mailing_model_real, record.ids)[record.id]

        new_sms_messages_sudo = self.env['sms.sms'].sudo().create([{'body': body, 'number': number, 'sms_account_id':sms_account} for number in sanitized_numbers])

        notification_messages = []
        if invalid_numbers:
            notification_messages.append(_('The following numbers are not correctly encoded: %s',
                ', '.join(invalid_numbers)))

        if notification_messages:
            message_body = Markup(
                f"<ul>{''.join('<li>%s</li>' for _ in notification_messages)}</ul>"
            ) % tuple(notification_messages)
            self.mailing_id._message_log(body=message_body)

        return True