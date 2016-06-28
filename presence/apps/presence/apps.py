from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals
from django.contrib.auth import get_user_model

def populate_users(sender, **kwargs):
    User = get_user_model()
    for i in range(10):
        username = "user_{}".format(i+1)
        email = "{}@example.com".format(username)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            is_staff=True,
                                            password="demo1234")

class PresenceConfig(AppConfig):
    name = 'apps.presence'

    def ready(self):
        signals.post_migrate.connect(populate_users, sender=self)