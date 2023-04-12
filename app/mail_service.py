from __future__ import print_function
import sib_api_v3_sdk
from django.conf import settings
from app.email_content import get_email_body


class SendinBlue_Mail_Service():
    def __init__(self):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = "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"

    def send_email(self, sender, to, race_distance="", cc=None, bcc=None, reply_to=None):
        subject = "Успешна регистрация"
        html_content = get_email_body()
        headers = {"Some-Custom-Name": "unique-id-1234"}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers,
            html_content=html_content, sender=sender, subject=subject
        )
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        api_response = api_instance.send_transac_email(send_smtp_email)
        return api_response

