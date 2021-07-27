from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created successfully! You can login now.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'title': 'Registration', 'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() or profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updates successfully!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'title': f'{request.user} | Tech Diary', 'user_update_form': user_update_form,
               'profile_update_form': profile_update_form}
    return render(request, 'users/profile.html', context)
