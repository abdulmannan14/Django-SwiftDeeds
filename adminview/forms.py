from django import forms
from register import models as register_models


#
#
# class RegisterForm(forms.Form):
#     first_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "First Name",
#                 "class": "form-control"
#             }
#         ))
#     last_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Last Name",
#                 "class": "form-control"
#             }
#         ))
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Username",
#                 "class": "form-control"
#             }
#         ))
#     email = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Email",
#                 "class": "form-control"
#             }
#         ))
#     phone = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Phone",
#                 "class": "form-control"
#             }
#         ))
#     sector = forms.ChoiceField(choices=register_models.sector_choices, label='Sector',
#                                widget=forms.Select(attrs={
#                                    "placeholder": "",
#                                    "class": "form-control fa fa-trash"
#
#                                })
#                                )
#     experience = forms.ChoiceField(choices=register_models.experience_choices, label='Experience (Years)',
#                                    widget=forms.Select(attrs={
#                                        "placeholder": "",
#                                        "class": "form-control"
#                                    })
#                                    )
#     Area = forms.ChoiceField(choices=register_models.area_choices, label='Area',
#                              widget=forms.Select(attrs={
#                                  "placeholder": "select",
#                                  "class": "form-control"
#                              })
#                              )
#
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 "placeholder": "Password",
#                 "class": "form-control"
#             }
#         ))
#     current_working_company = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Current Working Company",
#                 "class": "form-control"
#             }
#         ))
#     previous_working_company = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Previous Working Company",
#                 "class": "form-control"
#             }
#         ))


class UserForm(forms.ModelForm):
    class Meta:
        model = register_models.User
        fields = ['first_name', 'last_name', 'username', 'password']

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


class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = register_models.UserProfile
        fields = '__all__'
        exclude = ['user', 'current_working_company', 'previous_working_company', 'sector', 'area', 'experience',
                   'email_verified']

        # widgets = {
        #     "phone_no": forms.TextInput(attrs={"data_icon": "fa fa-link", "required": "required"}),
        #     "current_working_company": forms.TextInput(attrs={"data_icon": "fa fa-user", "required": "required"}),
        #     "previous_working_company": forms.TextInput(attrs={"data_icon": "fa fa-key", "required": "required"}),
        #     "experience": forms.Select(attrs={"data_icon": "fa fa-hashtag", "required": "required"}),
        #     "sector": forms.Select(attrs={"data_icon": "fa fa-hashtag", "required": "required"}),
        #     "area": forms.Select(attrs={"data_icon": "fa fa-hashtag", "required": "required"}),
        # }


class AddNewJobForm(forms.ModelForm):
    class Meta:
        model = register_models.UserProfile
        fields = "__all__"


class FilterForm(forms.ModelForm):
    class Meta:
        model = register_models.UserProfile
        fields = "__all__"
