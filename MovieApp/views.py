from django.forms import ValidationError 
from django.shortcuts import render , redirect
from MovieApp.models import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.db.models import Q
# Create your views here.



def anasayfa(request):
    """
    Giriş yapıldıktan sonraki anasayfayı getiren fonksiyondur
    film , tarih ve kategorileri listeler
    """
    if request.user.is_authenticated:
        _filmler = filmler.objects.all()
        _filmler = list(_filmler)
        _filmler.reverse()
        _kategori = kategoriler.objects.all()
        tarihler = range(1895,2023,1)
        tarihler=list(tarihler)
        tarihler.reverse()
        istenenSayfa = request.GET.get('sayfa', 1) #başta 1. sayfayı gösteriyoruz
        sayfalama = Paginator(_filmler, 16) #sayfalarda kaç nesne olacağını söylüyoruz
        try:
            secili_sayfaki_filmler = sayfalama.page(istenenSayfa)
        except PageNotAnInteger:
            secili_sayfaki_filmler = sayfalama.page(1)
        except EmptyPage:
            secili_sayfaki_filmler = sayfalama.page(sayfalama.num_pages)

        context={
            'filmler':secili_sayfaki_filmler,
            'kategoriler':_kategori,
            'tarihler':tarihler,
        }
        return render(request,'movie_templates/anasayfa.html',context)
    return redirect('welcome')



def film(request,slug):
    """
    Bu fonksiyon ilgili filmin kendi sayfasını , filmin kendisini getirir
    """
    film = filmler.objects.get(filmSlug=slug)
    film_kategoriler = filmler.objects.get(id=film.id).kategoriler.all()
    yapilanYorumlar = list(yorumlar.objects.filter(film_id = film.id ))
    yapilanYorumlar.reverse()
    context = {
        'film':film,
        'kategoriler':film_kategoriler,
        'yorumlar':yapilanYorumlar
    }
    if request.method == 'POST':
        yorum = request.POST['yorum']
        yeniYorum = yorumlar(yorum = yorum ,kullanici_id = User.objects.get(username=request.user.username).id , film_id=film.id)
        yeniYorum.save()
        context = {
            'film':film,
            'kategoriler':film_kategoriler,
            'yorumlar':yapilanYorumlar
        }
        return redirect('/umosTV/film_detay/{}'.format(slug))
    return render(request,'movie_templates/filmdetay.html',context)



def ara(request,id):
    """
    Bu fonksiyon önce tarihe göre arama yapmaya çalışır yapamaz ise string kategori bilgisine göre arama yapmaya çalışır
    """
    if request.user.is_authenticated:
        tarih1 = '{}-01-01'.format(id)
        tarih2 = '{}-12-31'.format(id)

        try : # Tarihe göre arama yaptırmaya çalış 
            arananFilm = filmler.objects.filter(Q(yapimYili__range =(tarih1,tarih2)))

        except ValidationError: # tarihe göre arama yapamadıysa kategori bilgisine göre arama yaptır
            arananFilm = filmler.objects.filter(kategoriler = kategoriler.objects.get(kategori=id).id)

        arananFilm = list(arananFilm)
        arananFilm.reverse()
        _kategori = kategoriler.objects.all()
        tarihler = range(1895,2023,1)
        tarihler=list(tarihler)
        tarihler.reverse()
        
        istenenSayfa = request.GET.get('sayfa', 1) #başta 1. sayfayı gösteriyoruz
        sayfalama = Paginator(arananFilm, 16) #sayfalarda kaç nesne olacağını söylüyoruz
        try:
            secili_sayfaki_filmler = sayfalama.page(istenenSayfa)

        except PageNotAnInteger:
            secili_sayfaki_filmler = sayfalama.page(1)

        except EmptyPage:
            secili_sayfaki_filmler = sayfalama.page(sayfalama.num_pages)

        context={
            'filmler':secili_sayfaki_filmler,
            'kategoriler':_kategori,
            'tarihler':tarihler,
            'aranan':id,
        }
        return render(request,'movie_templates/search.html',context)
    return redirect('welcome')



def ara2(request):
    """
    Bu fonksiyon ise search bara girilen veriye göre arama yapar
    """
    if request.user.is_authenticated:

        if request.method =='POST':
            arananKelime = request.POST['arananKelime']
            arananFilm = filmler.objects.filter(filmAdi__icontains = arananKelime)
            arananFilm = list(arananFilm)
            arananFilm.reverse()
            _kategori = kategoriler.objects.all()
            tarihler = range(1895,2023,1)
            tarihler=list(tarihler)
            tarihler.reverse()
            istenenSayfa = request.GET.get('sayfa', 1) #başta 1. sayfayı gösteriyoruz
            sayfalama = Paginator(arananFilm, 16) #sayfalarda kaç nesne olacağını söylüyoruz

            try:
                secili_sayfaki_filmler = sayfalama.page(istenenSayfa)
            except PageNotAnInteger:
                secili_sayfaki_filmler = sayfalama.page(1)
            except EmptyPage:
                secili_sayfaki_filmler = sayfalama.page(sayfalama.num_pages)
                
            context={
                'filmler':secili_sayfaki_filmler,
                'kategoriler':_kategori,
                'tarihler':tarihler,
                'aranan':arananKelime
            }
            return render(request,'movie_templates/search.html',context)
        return redirect('welcome')
    return redirect('welcome')