from django.core.mail import EmailMessage

from trashradar.celery import app


@app.task(name='send_mail')
def send_mail(recipient_list, template_name, substitution_data, blind_recipient_list=None):
    """
    Just send an email with Sparkpost (Sparkpost Template)
    :param recipient_list: list
    :param template_name: str
    :param substitution_data: dict
    :param blind_recipient_list: list
    :return:
    """
    if not blind_recipient_list:
        blind_recipient_list = []

    msg = EmailMessage(
        to=[
            {'address': recipient, 'substitution_data': substitution_data}
            for recipient in recipient_list
        ],
        bcc=blind_recipient_list
    )
    msg.template = template_name
    msg.send()
