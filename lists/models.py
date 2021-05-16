from django.db import models


# Create your models here.
class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    priority = models.TextField(default='prioridade média')
    list = models.ForeignKey(List,on_delete=models.SET_DEFAULT,default=None)
