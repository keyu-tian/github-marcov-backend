from django.db import models


class Knowledge(models.Model):
    title = models.TextField()
    body = models.TextField()

