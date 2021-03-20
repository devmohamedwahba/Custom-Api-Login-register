from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('sms-reset/', views.TokenResetView.as_view(), name='sms-reset'),
    path('verify/', views.VerifyUserView.as_view(), name='verify'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]
