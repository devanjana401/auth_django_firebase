from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        mobile = request.POST['mobile']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, mobile=mobile)
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'signup.html')
def log(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')
    return render(request, 'login.html')
@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})

def forgot_password(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        new_password = request.POST.get('new_password')
        try:
            profile = UserProfile.objects.filter(mobile=mobile).first()
            user = User.objects.get(username=profile.user.username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please log in.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Mobile number not registered.")
    return render(request, 'forgot_password.html')
def login_with_otp(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        profile = UserProfile.objects.filter(mobile=mobile).first()
        if profile:
            user = profile.user
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Mobile number not registered.")
            return redirect('login_with_otp')
    return render(request, 'login_with_otp.html')
@csrf_exempt
def check_user_exists(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if UserProfile.objects.filter(mobile=mobile).exists():
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})
    return JsonResponse({'error': 'Invalid method'}, status=400)

