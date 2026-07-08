from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'autocomplete': 'off'
            }),
            'last_name': forms.TextInput(attrs={
                'autocomplete': 'off'
            }),
            'username': forms.TextInput(attrs={
                'autocomplete': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'email'
            }),
        }


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match."
            )    