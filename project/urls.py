from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),

]


handler404 = 'utils.views.handler404'
handler500 = 'utils.views.handler500'
