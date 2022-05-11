from django.shortcuts import  render , redirect
from AccountApp.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout 
from MovieApp.models import *
from AccountApp.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
# Create your views here.



def welcome(request):
    """
    Üye girişi yapmamış kişileri herkesin girebildiği 
    varsayılan ana sayfaya yönlendirir
    """
    return render(request,'account_templates/anasayfa.html')



def register(request):
    """
    Kayıt olma fonksiyonu
    """
    if request.user.is_authenticated:
        return redirect('anasayfa')

    form = uyelik_Tipi_Form(request.FILES or None)

    if request.method=='POST':
        username = request.POST['_username']
        password = request.POST['_password']
        password2 = request.POST['_password2']
        email = request.POST['_email']
        secilenUyelikTipi = request.POST['uyelikTipi']#django form
        context={
            'form':form,
            'username':username,
            'email':email,
            'secilenUyelikTipi':secilenUyelikTipi
        }

        if password==password2: #Girilen Şifreler Aynı

            if len(password)<8: # Girilen Şifreler Aynı ama 8 haneden kısalar
                context['hata']='Şifre 7 haneden Büyük olmalı'
                return render(request , 'account_templates/kayit.html',context)

            elif len(password)>=8: # Girilen şifreler aynı ve 8 hanedende büyükler
                yeniKullanici = User(username=username,email=email)
                yeniKullanici.set_password(password)

                try : # Şifreler aynı ve 7 haneden büyük ayrıca kullanıcı adıda müsait
                    if User.objects.filter(email = email): # Şifreler aynı ve 7 haneden büyük ayrıca kullanıcı adıda müsait ama email müsait değil
                        context['hata']='Girilen email adresi müsait değil'
                        return render(request , 'account_templates/kayit.html',context)
                    else : # Tüm şartlar sağlandı , şifreler aynı ve uzunluğu 7'den büyük , email ve kullanıcı adı müsait
                        yeniKullanici.save()
                        yeniUyelikKayit = uyelik(uyelikTipi = secilenUyelikTipi,kullanici_id = User.objects.get(username = username).id)
                        yeniUyelikKayit.save()
                        login(request,yeniKullanici)
                        return redirect('anasayfa')

                except IntegrityError: # Şifreler aynı ve 7 haneden büyük ama kullanıcı adı müsait değil #
                    context['hata']='Girilen Kullanıcı Adı Daha Önce Alınmış'
                    return render(request , 'account_templates/kayit.html',context)
            else :
                return redirect('welcome')

        else : # Girilen Şifreler Aynı Değil
            context['hata']='Girilen şifreler farklı'
            return render(request , 'account_templates/kayit.html',context)

    return render(request , 'account_templates/kayit.html',{'form':form})



def sign_in(request):
    """
    Giriş Yapma fonksiyonumuz
    """
    if request.user.is_authenticated:
        return redirect('anasayfa')
    form = girisForm(request.POST or None)

    if form.is_valid():
        kullaniciAdi=form.cleaned_data.get('kullanici')
        sifre = form.cleaned_data.get('sifre')
        kullanici = authenticate(username=kullaniciAdi,password=sifre)
        context={
            'username':kullaniciAdi,
            'form':form,
        }
        
        if kullanici is None : # Böyle Bir kullanıcı yoksa hata ver sayfayı yenile
            context['hata'] = 'Kullanıcı Adı veya Şifre Yalnış'
            return render(request , 'account_templates/giris.html',context)

        login(request,kullanici)
        return redirect('anasayfa')

    return render(request , 'account_templates/giris.html',{'form':form})



def sign_out(request):
    """
    Çıkış yapma fonksiyonumuz
    """
    logout(request)
    return redirect('welcome')



def password_change(request):
    """
    şifre değiştirme fonksiyonumuz
    """
    if request.method =='POST':
        yeniSifre = request.POST['yeniSifre']
        aktifKullanici = User.objects.get(username=request.user.username)
        aktifKullanici.set_password(yeniSifre)
        aktifKullanici.save()
        return redirect('sign_in')
    return redirect('/profil/{}'.format(request.user.username))



def profile(request,username):
    """
    Giriş yapmış kullanıcılar için profil sayfasını getiren fonksiyonumuz
    """
    if request.user.is_authenticated :
        uye = User.objects.get(username=username)
        if request.user.username == uye.username : 
            """
            bu if bloğunun amacı bir üye girişliyken url kısmından başka bir üyenin profil bağlantısını
            girip başka bir profili görüntülemeye çalışırsa çalışamasın diye . Eğer giriş yapılmış kullanıcının
            kendi profil sayfası görüntülenmeye çalışılıyorsa problem yok ancak başka bir profili görmek için
            bir istekte bulunursa else bloğunda return redirect('/profil/{}'.format(request.user.username)) kısmı
            ile o an giriş yapmış olan hesabın profil bağlantısına yönlendirme yapılır
            """
            yapilanYorumlar = yorumlar.objects.filter(kullanici=uye.id)
            
            """
            Aşağıdaki try except yapısı superuserlara ve moderatör panelinden eklenen
            standart userlara otomatik bir uyelik tipi atamak içindir 
            """
            try:
                uyelik_ = uyelik.objects.get(kullanici_id = uye.id)
            except ObjectDoesNotExist :
                uyelik_ = uyelik(kullanici_id = User.objects.get(username=uye.username).id , 
                uyelikTipi='Standart Üye 15$')
                uyelik_.save()
            context={
                'uye':uye,
                'yorumlar':yapilanYorumlar,
                'uyelik':uyelik_,
            }
            if request.method=='POST': # Yorum Sil bloğu
                silinecekYorum_id = request.POST['silinecekYorum']
                yorumlar.objects.get(id=silinecekYorum_id).delete()
                return redirect('/profil/{}'.format(username))
        else :
            return redirect('/profil/{}'.format(request.user.username))
        return render(request,'account_templates/profil.html',context)