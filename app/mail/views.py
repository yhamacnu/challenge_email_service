"""
Views for the mail app
"""
from django.shortcuts import render
from django.core.mail import send_mail, get_connection, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from sparkpost.exceptions import SparkPostAPIException
from .forms import EmailForm

SENDGRID_BACKEND = "sgbackend.SendGridBackend"
SES_BACKEND = "django_ses.SESBackend"


def email(request):
    """
    Handles requests/responses for the mail app's EmailForm
    """
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            mail_form = {"from": form.cleaned_data["from_email_address"],
                         "to": form.cleaned_data["to_email_address"],
                         "subject": form.cleaned_data["subject"],
                         "message":form.cleaned_data["message"]}
            to_send = [email.strip() for email in mail_form["to"].split(";")]
            send_success_cnt = 0
            try:
                sendgrid_backend = get_connection(SENDGRID_BACKEND,
                                                  api_key=settings.SENDGRID_API_KEY)
                send_success_cnt = send_mail(mail_form["subject"],
                                             mail_form["message"],
                                             mail_form["from"],
                                             to_send,
                                             connection=sendgrid_backend)
            except SparkPostAPIException:
                # failover handling example, e.g. unconfigured sending domain code: 7001
                ses_backend = get_connection("django_ses.SESBackend")
                send_success_cnt = send_mail(mail_form["subject"],
                                             mail_form["message"],
                                             mail_form["from"],
                                             to_send,
                                             connection=ses_backend)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            except Exception:
                return HttpResponse("Something went wrong. Contact admin.")
            else:
                if send_success_cnt == 1:
                    return HttpResponse("Send was successful.")
                else:
                    return HttpResponse("Send was NOT successful.")
        return render(request, "mail/mail.html", {"form":form})
    return render(request, "mail/mail.html", {"form":form})
