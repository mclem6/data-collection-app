from django import forms

from .models import User


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class CodeForm(forms.Form):
    code = forms.RegexField(regex=r"^\d{6}$", error_messages={"invalid": "Enter the 6-digit code."})


class OnboardingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "dialect"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["dialect"].required = True