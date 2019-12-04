from django.db import models
from django.urls import reverse

class Input(models.Model):
    source = models.CharField(max_length=100, default='')
    destination = models.CharField(max_length=100, default='')
    date = models.CharField(max_length=100, default='')

    def  __str__(self):
        return 'SD- 1%s' % self.id
