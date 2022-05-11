from typing_extensions import Required
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class diller(models.Model):
    dil = models.CharField(max_length=15,unique=True,verbose_name='Dil\'i Girin :')
    def __str__(self) :
        return self.dil
    class Meta:
        verbose_name = 'Dil'
        verbose_name_plural = 'Diller'
class kategoriler(models.Model):
    kategori = models.CharField(max_length=30,verbose_name='Kategoriyi Girin :',unique=True)
    def __str__(self) :
        return self.kategori
    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

kaliteler=[
    ('144px','144px'),
    ('240px','240px'),
    ('360px','360px'),
    ('480px','480px'),
    ('720px','720px'),
    ('1280px','1280px'),
]

class filmler(models.Model):
    filmAdi=models.CharField(max_length=50,null=False,verbose_name='Film Adı :')
    filmKonusu=models.TextField(max_length=500,null=True,blank=True,verbose_name='Konu :')
    film=models.FileField(upload_to='movies/',verbose_name='Filmi yükle :',null=False,)
    filmPoster=models.FileField(upload_to='posters/',verbose_name='Film Posteri :',null=True,blank=True)
    filmSlug=models.SlugField(null=False,unique=True)
    ulke = models.CharField(max_length=85,verbose_name='Ülke Adını Girin :')
    yapimYili = models.DateField(null=True)
    kalite = models.CharField(choices=kaliteler,max_length=8)
    kategoriler = models.ManyToManyField(kategoriler)
    diller = models.ManyToManyField(diller)
    def __str__(self) :
        return self.filmAdi
    class Meta:
        verbose_name = 'Film'
        verbose_name_plural = 'Filmler'

class yorumlar(models.Model):
    kullanici = models.ForeignKey(User,on_delete=models.CASCADE)
    yorum = models.TextField(max_length=500)
    film = models.ForeignKey(filmler,on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'
    def __str__(self):
        return self.kullanici.username +' | '+ self.film.filmAdi
"""
film tablosu ---
film adı
konusu
Video
YapımYılı
Poster
Ulke
Diller()
kategori()
Yorumlar()
"""
