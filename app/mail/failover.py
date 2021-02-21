"""
Mail send handling interface in same module as
implementation, for illustrative purposes.
"""
from abc import ABCMeta, abstractstaticmethod
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.http import HttpResponse
from sparkpost.exceptions import SparkPostAPIException


class MailSendHandler(metaclass=ABCMeta):
    """Mail handling interface."""

    @abstractstaticmethod
    def set_failover(backup_handler):
        """Failover backend."""

    @abstractstaticmethod
    def handle_send(mail_form):
        """Handle sending."""


class SparkPostHandler(MailSendHandler):
    """Handles primary sending backend provided by SparkPost."""

    SPARKPOST_BACKEND = "sparkpost.django.email_backend.SparkPostEmailBackend"

    def __init__(self):
        self._failover = None

    def set_failover(self, backup_handler):
        """Sets the failover mail send handler."""
        self._failover = backup_handler

    def handle_send(self, mail_form):
        """
        Handles the sending and encapsulates the failover triggers, i.e.
        failover conditions.
        NB: Just for illustrative purposes, only one trigger.
        """
        sparkpost_backend = get_connection(self.SPARKPOST_BACKEND,
                                           settings.SPARKPOST_API_KEY)
        try:
            ret = send_mail(mail_form["subject"],
                      mail_form["message"],
                      mail_form["from"],
                      [mail_form["to"]],
                      connection=sparkpost_backend)
            if ret == 0:
                self._failover.handle_send(mail_form)
        except SparkPostAPIException:
            # handling as an example a only specific fail event,
            # e.g. unconfigured sending domain code: 7001
            self._failover.handle_send(mail_form)


class SESHandler(MailSendHandler):
    """Handles primary sending backend provided by AWS SES."""

    SES_BACKEND = "django_ses.SESBackend"

    def __init__(self):
        self._failover = None

    def set_failover(self, backup_handler):
        """Sets the failover mail send handler."""
        self._failover = backup_handler

    def handle_send(self, mail_form):
        """
        Handles the sending and encapsulates the failure handling.
        """
        ses_backend = get_connection(self.SES_BACKEND)
        try:
            send_mail(mail_form["subject"],
                      mail_form["message"],
                      mail_form["from"],
                      [mail_form["to"]],
                      connection=ses_backend)
        except Exception:
            HttpResponse("Something went wrong. Contact admin.")


class EmailProviderChain:
    """Email provider failover chain."""

    def __init__(self):
        self.main = SparkPostHandler()
        self.failover1 = SESHandler()
        # single failover provider only
        self.main.set_failover(self.failover1)

    def send(self, mail_form):
        """
        Processes the mail form from the view,
        according to the failover chain.
        """
        self.main.handle_send(mail_form)
