from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class StravaUser(models.Model):
    uid = models.ForeignKey(User)
    access_token = models.CharField(editable=False, max_length=120)

    def __str__(self):
        self.access_token