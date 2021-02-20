from django import forms


class EmailForm(forms.Form):
    """
    Stores the fields for the mailt to be send.
    """
    from_email_address = forms.EmailField(max_length = 200)
    to_email_address = forms.EmailField(max_length = 200)
    subject = forms.CharField(max_length = 50)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)
