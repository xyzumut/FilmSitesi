
from django.urls import path , include
from MovieApp.views import *


urlpatterns = [
    path('anasayfa/',anasayfa,name='anasayfa'),
    path('film_detay/<slug:slug>',film),
    path('ara/<str:id>',ara),
    path('ara/',ara2,name='ara2'),
]


