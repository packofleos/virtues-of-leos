from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm

def register(request):
    """View for registering the user."""

    if request.method != 'POST':
        form = RegistrationForm()

    else:
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            created_user = form.save()
            # registered users are guests, until verified by a staff
            guest_group = Group.objects.get(name='guest')
            created_user.groups.add(guest_group)
            login(request, created_user)
            return redirect('virtues:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def user_settings(request):
    user_links = {
        'email': reverse('account_email'),
        'change password': reverse('account_change_password'),
        'reset password': reverse('account_reset_password'), 
    }
    return render(request, 'users/user_settings.html', context={'user_links': user_links})