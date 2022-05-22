from django.db import models


class Tred(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.FileField(upload_to="files/posts/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

