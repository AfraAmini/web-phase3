from django import forms

from user.models import BlogUser


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20, required=True)
    email = forms.EmailField(required=True)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        q = BlogUser.objects.filter(email=cleaned_data.get("email")).count()
        if q > 0:
            raise forms.ValidationError("This email has been used before")
        return cleaned_data
