from django.contrib import admin
from AccountApp.models import *
from MovieApp.models import *
# Register your models here.

admin.site.register(filmler)
admin.site.register(diller)
admin.site.register(kategoriler)
admin.site.register(yorumlar)
admin.site.register(uyelik)



admin.site.site_header='UmosTV Moderatör Paneli'
admin.site.index_title='UmosTV Yönetim Paneli'