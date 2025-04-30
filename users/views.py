from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from posts.models import Post

from django.http import HttpResponseRedirect

# ===============================================================

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                subject='Welcome to Social Media Lite',
                message='Thank you for signing up',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True
            )
            return redirect('feed')

    else:
        form = CustomUserCreationForm()
        return render(request, 'users/signup.html', {'form' : form})
    

# =================================================================

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if next_url in [None, '', 'None']:
        next_url = None  # normalize bad values to None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('feed')

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form, 'next': next_url})


# ==================================================================


def logout_view(request):
    logout(request)
    return redirect('login')


# ==================================================================

@login_required
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    post_count = posts.count()

    return render(request, 'users/profile.html', {
        'user': user,
        'posts': posts,
        'post_count': post_count
    })