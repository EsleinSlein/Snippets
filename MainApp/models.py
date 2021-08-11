import datetime
from django.contrib.auth.models import User
from django.db import models

LANG_CHOICES = (
    ("py", "python"),
    ("js", "javascript"),
    ("cpp", "C++"),

)


class Snippet(models.Model):
    name = models.CharField(max_length=100,)
    lang = models.CharField(max_length=30, choices=LANG_CHOICES, null=True)
    code = models.TextField(max_length=5000, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
