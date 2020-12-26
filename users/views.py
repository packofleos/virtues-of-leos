from django.contrib.auth import login
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
            login(request, created_user)
            return redirect('virtues:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)