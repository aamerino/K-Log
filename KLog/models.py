from django.db import models


class Log(models.Model):
    level = models.CharField(max_length=30)
    error_class = models.CharField(max_length=30)
    date = models.DateTimeField

