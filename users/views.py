from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import FormView

from users.forms import LoginForm, RegisterModelForm


# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:index')
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Disabled account'
                    )
                    return render(request, 'users/login.html')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Username or Password invalid'
                )
                return render(request, 'users/login.html')

    return render(request, 'users/login.html', {'form': form})


def register_page(request):
    form = RegisterModelForm()
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user.save()
            send_mail(
                'Hello Dear!',
                'You Successfully registered',
                'jasurmavlonov24@gmail.com',
                [user.email],
                fail_silently=False
            )
            login(request, user)
            return redirect('shop:index')
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:index')


class RegisterPage(FormView):
    template_name = 'users/register.html'
    form_class = RegisterModelForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(user.password)
        user.save()
        send_mail(
            'Hello Dear!',
            'You Successfully registered',
            'jasurmavlonov24@gmail.com',
            [user.email],
            fail_silently=False
        )
        login(request, user)
        return redirect('shop:index')

    def form_invalid(self, form):
        pass
