from typing import List

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend


def send_email(subject: str,
               message: str,
               to_email_list: List[str],
               attachment=None,
               attachment_name: str = "",
               attachment_type: str = "") -> None:
    """
    A Function to send emails to user
    """
    try:
        if isinstance(to_email_list, str):
            to_email_list = [to_email_list]
        mail_host = settings.EMAIL_HOST
        mail_username = settings.EMAIL_HOST_USER
        mail_password = settings.EMAIL_HOST_PASSWORD
        mail_port = int(settings.EMAIL_PORT)
        from_email = settings.EMAIL_HOST_USER
        use_tls = settings.EMAIL_USE_TLS
        backend = EmailBackend(host=mail_host,
                               port=mail_port,
                               username=mail_username,
                               password=mail_password,
                               use_tls=use_tls,
                               fail_silently=False)
        email = EmailMessage(subject=subject,
                             body=message,
                             from_email=from_email,
                             to=to_email_list,
                             connection=backend,
                             bcc=[])
        if attachment:
            email.attach('{}'.format(attachment_name), attachment,
                         '{}'.format(attachment_type))
        email.content_subtype = 'html'
        email.send()
        print('email sent to', to_email_list)
    except Exception as e:
        print('Error in sending an email : ', e)
        pass