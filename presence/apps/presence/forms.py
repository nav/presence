from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
import names

def generate_username():
    return names.get_full_name().lower().replace(' ', '.')

class OpenAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, initial=generate_username)
    password = forms.CharField(label=_("Password"), required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = "demo1234"

        if username and password:
            User = get_user_model()
            users = User.objects.filter(username=username)
            if users.exists():
                user = users.first()
                user.set_password(password)
                user.save()
            else:
                User.objects.create_user(username=username,
                                         email="{}@example.com".format(username),
                                         password=password)

            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
