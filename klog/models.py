from django.db import models


class Log(models.Model):
    exception_name = models.CharField(max_length=30)
    error_class = models.CharField(max_length=30)
    date_time = models.DateTimeField()

