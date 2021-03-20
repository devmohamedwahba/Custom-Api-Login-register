from django.core.mail import EmailMessage
from smtplib import SMTPException
import wget
import os
import logging

logger = logging.getLogger(__name__)


class SaveAttach:
    def __init__(self, attach, email):
        self.attach = attach
        self.email = email

    def save_file(self):
        file_url = self.attach.document
        file_name = wget.download(file_url)
        self.email.attach_file(file_name)
        os.remove(file_name)


class Email:
    def __init__(self, receiver, sender, subject, body, attachments=None):
        self.receiver = receiver
        self.sender = sender
        self.subject = subject
        self.body = body
        self.attachments = attachments

    def send(self):
        email = EmailMessage(subject=self.subject, body=self.body, from_email=self.sender, to=[self.receiver])
        email.content_subtype = 'html'
        if self.attachments:
            for attach in self.attachments.all():
                try:
                    # Create Object of Save Attach Class
                    save_attach = SaveAttach(attach=attach, email=email)
                    save_attach.save_file()
                except Exception as e:
                    print('There was an error attach file to  an email: ', e)

        try:
            return email.send()
        except SMTPException as e:
            logger.exception({e})
