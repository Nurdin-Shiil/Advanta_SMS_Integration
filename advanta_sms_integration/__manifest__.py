
{
    "name": " SMS Advanta Integration ",
    "summary": "Send SMS using Advanta Credentials",
    "version": "18.0.1.0.0",
    "author": "Nurdin Ismail", 
    "website": "https://code.ke",
    "category": "Extra Tools",
    "depends": ["base","sms", 'mass_mailing', 'mass_mailing_sms'],
    "license": "LGPL-3",
    "data": [
        'security/ir.model.access.csv',
        "views/sms_account_views.xml",
        "views/sms_form_and_wizard.xml",
    ],
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "development_status": "Mature",
}
