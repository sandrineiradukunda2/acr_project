from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.utils import timezone



# Create your views here.
def user_list(request):
    users = users.objects.all()  # Fixed typo: 'object' → 'objects'
    return render(request, 'user_list.html', {'users': users})
    users = User.object.all()
    return


# View for login functionality
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user with provided credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('home')  # Redirect to home page or any other page
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password")
    
    # Render the login template when the form is not submitted
    return render(request, 'login.html')



def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob') or timezone.now()
        
        profile_picture = request.FILES.get('profile_picture')

        # Validation
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'registration.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'registration.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return render(request, 'registration.html')

       

        # Save user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password1),
            gender=gender,
            dob=dob,
           
            profile_picture=profile_picture
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'registration.html')
def base(request):
    return render(request, 'base.html')
