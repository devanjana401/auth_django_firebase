from django.urls import path
from.import views

urlpatterns = [
    path('', views.index,name="index"),
    path('signup/', views.signup,name="signup"),
    path('login/', views.log,name="login"),
    path('home/', views.home,name="home"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
]