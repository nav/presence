from __future__ import unicode_literals

from django.db import models
from django_comments.models import Comment

class Message(models.Model):
    page = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    comment = models.OneToOneField(Comment, blank=True)
