from django.urls import path
from.import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.signup,name="signup"),
    path('', views.log,name="login"),
    path('home/', views.home,name="home"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login_with_otp/', views.login_with_otp, name="login_with_otp"),
    path('check-user/', views.check_user_exists, name='check_user_exists'),


]