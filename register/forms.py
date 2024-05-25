from django import forms
from . import models as register_models


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))


    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))



class UserForm(forms.ModelForm):
    class Meta:
        model = register_models.User
        fields = ['first_name', 'last_name']

        widgets = {
            # "first_name": forms.TextInput(attrs={"data_icon": "fa fa-link", "required": "required"}),
            # "last_name": forms.TextInput(attrs={"data_icon": "fa fa-user", "required": "required"}),
            # "username": forms.TextInput(attrs={"data_icon": "fa fa-key", "required": "required"}),
            # "email": forms.TextInput(attrs={"data_icon": "fa fa-key", "required": "required"}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = register_models.UserProfile
        fields = '__all__'
        exclude = ['user']

        # widgets = {
        #     "phone_no": forms.TextInput(attrs={"data_icon": "fa fa-link", "required": "required"}),
        #     "current_working_company": forms.TextInput(attrs={"data_icon": "fa fa-user", "required": "required"}),
        #     "previous_working_company": forms.TextInput(attrs={"data_icon": "fa fa-key", "required": "required"}),
        #     "experience": forms.Select(attrs={"data_icon": "fa fa-hashtag", "required": "required"}),
        #     "sector": forms.Select(attrs={"data_icon": "fa fa-hashtag", "required": "required"}),
        #     "area": forms.Select(attrs={"data_icon": "fa fa-hashtag", "required": "required"}),
        # }
