from django.urls import path
from AccountApp.views import *
urlpatterns = [
    path('', welcome,name='welcome'),
    path('kayit_ol/',register ,name='register'),
    path('giris/',sign_in,name='sign_in'),
    path('cikis/',sign_out,name='sign_out'),
    path('degis/',password_change,name='password_change'),
    path('profil/<str:username>/',profile,name='profil'),
]
