"""
Views for the mail app
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from .forms import EmailForm
from .failover import EmailProviderChain


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
            chain = EmailProviderChain()
            try:
                chain.send(mail_form)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            except Exception:
                return HttpResponse("Something went wrong. Contact admin.")
        return render(request, "mail/mail.html", {"form":form})
    return render(request, "mail/mail.html", {"form":form})
