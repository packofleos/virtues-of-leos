from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

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