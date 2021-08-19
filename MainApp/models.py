import datetime
from django.contrib.auth.models import User
from django.db import models
from MainApp.formatChecker import ContentTypeRestrictedFileField

LANG_CHOICES = (
    ("py", "python"),
    ("js", "javascript"),
    ("cpp", "C++"),
)


class Snippet(models.Model):
    name = models.CharField(max_length=100, )
    lang = models.CharField(max_length=30, choices=LANG_CHOICES, null=True)
    code = models.TextField(max_length=5000, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    public = models.BooleanField(default=True,)


class Comment(models.Model):
    text = models.TextField(max_length=2000, null=True, blank=True,)
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    snippet = models.ForeignKey(to='Snippet', on_delete=models.CASCADE, related_name="comments")
    image = ContentTypeRestrictedFileField(upload_to="images", max_upload_size=104857600,   content_types=['image/jpeg',  'image/png'], null=True, blank=True)


    def __str__(self):
        return f"Snippet: {self.name}"