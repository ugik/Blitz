from django import forms
from django.contrib.auth.models import User

class NewMessageForm(forms.Form):

    to_user = forms.CharField(max_length=100)
    message_content = forms.CharField(max_length=10000)

    def clean_to_user(self):
        data = self.cleaned_data['to_user']
        data = User.objects.get(pk=int(data))
        return data
