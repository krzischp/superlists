from django.db import models

# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')
    priority = models.TextField(default='prioridade média')
