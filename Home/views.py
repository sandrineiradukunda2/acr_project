from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import OTP, User
from django.http import JsonResponse
from datetime import datetime






# Create your views here.
def user_list(request):
    users = User.objects.all()  # Fixed typo: 'object' → 'objects'
    return render(request, 'user_list.html', {'users': users})
    
    


# View for login functionality
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user with provided credentials
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('home')  # Redirect to home page or any other page
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid email or password")
    
    # Render the login template when the form is not submitted
    return render(request, 'login.html')




def register_view(request):
    print("Register view called")
    if request.method == 'POST':
        print("POST request received")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_picture = request.FILES.get('profile_picture')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return HttpResponse("Passwords do not match.")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return HttpResponse("Username already exists.")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return HttpResponse("Email already in use.")

        # FIX: Create a proper user instance instead of overwriting `User`
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password1),
        )

        # Assign additional attributes (if using a custom User model, adjust accordingly)
        user.verification_token = uuid.uuid4()
        user.token_expiry = timezone.now() + timedelta(minutes=30)
        user.is_verified = False
        print(f"User created: {user}")
        user.save()

        # FIX: Use the correctly assigned `user` variable
        verification_link = request.build_absolute_uri(
            reverse('verify_email', args=[user.verification_token])
        )
        print(f"Verification link: {verification_link}")
        subject = "Verify Your Email Address"
        message = f"""
        Hi {user.first_name},

        Thanks for registering!

        Please verify your email using the link below. 
        ⚠️ This link will expire in 30 minutes. If you do not verify your account, it will be deleted.

        🔗 Verify Email: {verification_link}

        Regards,
        Your Team
        """

        send_mail(subject, message, 'noreply@example.com', [user.email])

        messages.success(request, "Check your email to verify your account. The link will expire in 30 minutes.")
        return redirect('login')

    return render(request, 'registration.html')


def verify_email(request, token):
    user = get_object_or_404(User, verification_token=token)

    if timezone.now() > user.token_expiry:
        user.delete()
        messages.error(request, "Verification link expired. Account deleted.")
        return redirect('register')

    user.is_verified = True
    user.save()
    messages.success(request, "Email verified successfully! You can now log in.")
    return redirect('login')



def send_otp(user_email):
    user = get_object_or_404(User, email=user_email)
    otp_instance = OTP.objects.create(user=user)
    otp_instance.generate_otp()

    send_mail(
        'Your Login OTP',
        f'Use this OTP to verify your login: {otp_instance.otp_code}. This code expires in 5 minutes.',
        'your-email@example.com',
        [user.email],
        fail_silently=False,
    )

def verify_otp(request):
    user_email = request.POST.get('email')
    otp_code = request.POST.get('otp')

    user = get_object_or_404(User, email=user_email)
    otp_instance = OTP.objects.filter(user=user, otp_code=otp_code).last()

    if otp_instance and otp_instance.expires_at > datetime.now():
        return JsonResponse({"message": "OTP verified successfully!"})
    else:
        return JsonResponse({"error": "Invalid or expired OTP!"}, status=400)

def base(request):
    return render(request, 'base.html')
