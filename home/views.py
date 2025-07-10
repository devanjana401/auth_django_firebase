from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
# Create your views here.
def index(request):
    return render(request,'index.html')
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
        return redirect('login')  # or wherever you want to go after signup

    return render(request, 'signup.html')
def log(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')  # Change 'home' to your home view name
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Change 'login' to the correct URL name

    return render(request, 'login.html')
@login_required
def home(request):
    return render(request, 'home.html')
def forgot_password(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')

        # ✅ OPTIONAL: Verify OTP on frontend using Firebase before this step

        try:
            # Find user by mobile number (assuming mobile stored in `User.username` or use custom User model)
            user = User.objects.get(username=mobile)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please log in.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Mobile number not registered.")
    
    return render(request, 'forgot_password.html')

