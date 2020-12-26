from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # we don't want any help text
        for field in self.fields.values():
            field.help_text = None

        self.fields['password2'].label = "Confirm"

    def save(self, *arsg, **kwargs):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if kwargs.get('commit', True):
            user.save()

        return user
