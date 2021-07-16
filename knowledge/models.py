from django.db import models


class Knowledge(models.Model):
    title = models.TextField()
    body = models.TextField()
    source = models.CharField(max_length=128, default="未知")


class EpidemicPolicy(models.Model):
    title = models.TextField()
    datetime = models.DateTimeField()
    body = models.TextField()
    src = models.TextField()

    class Meta:
        ordering = ['-datetime']
