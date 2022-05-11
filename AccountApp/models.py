from django.db import models
from django.contrib.auth.models import User , Group
# Create your models here.

uyelik_tipleri = [
    ('Deneme Sürümü','Deneme Sürümü 3$'),
    ('Standart Üye','Standart Üye 15$'),
]

class uyelik(models.Model):
    uyelikTipi = models.CharField(choices=uyelik_tipleri,max_length=15,verbose_name='')
    kullanici = models.OneToOneField(User,on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Üyelik Tipi'
        verbose_name_plural = 'Üyelik Tipleri'
    def __str__(self) :
        return self.kullanici.username+' : '+self.uyelikTipi
