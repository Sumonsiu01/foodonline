from django import forms
from .models import User, UserProfile


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

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing your address...','required': 'required'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), required=False)
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), required=False)

    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 
            'pin_code', 'latitude', 'longitude'
        ]

    # __init__ মেথডটি অবশ্যই UserProfileForm ক্লাসের ভেতরে ইনডেন্ট করে রাখতে হবে
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['latitude', 'longitude']:
                self.fields[field].widget.attrs['readonly'] = 'readonly'