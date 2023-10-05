import random
import uuid

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse
from django.views import View

from . import forms
from django.views.generic import FormView
from . import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class ContactUsView(LoginRequiredMixin, FormView):
    template_name = 'account_app/contact.html'
    form_class = forms.ContactUsForm
    success_url = '/'

    def form_valid(self, form):
        email = self.request.user.email
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        message = message + '/' + email
        send_mail(subject, message, 'rezasharafdini973@gmail.com', ['rezasharafdini973@gmail.com'], fail_silently=False)
        return super().form_valid(form=form)

    def form_invalid(self, form):
        messages.error(self.request, 'The email was not sent')
        return self.render_to_response(self.get_context_data(form=form))


class AboutView(View):
    def get(self, request):
        return render(request, 'account_app/about.html', {})


class LoginView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        form = forms.LoginForm()
        return render(request, 'account_app/login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        next_page = request.GET.get('next')
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user:
                login(request, user)
                if next_page:
                    return redirect(next_page)

                return redirect('/')
            form.add_error('email', 'user of email invalid.')
        form.add_error('email', 'email or password is wrong.')
        return render(request, 'account_app/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        form = forms.RegisterForm()
        return render(request, 'account_app/register.html', {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if models.User.objects.filter(email=cd['email']):
                messages.error(request, 'email valid.')
                return render(request, 'account_app/register.html', {'form': form})

            if models.User.objects.filter(full_name=cd['username']):
                messages.error(request, 'username valid.')
                return render(request, 'account_app/register.html', {'form': form})

            token = str(uuid.uuid4())
            randcode = random.randint(10000, 99999)
            print(randcode)
            send_mail('code', str(randcode), 'rezasharafdini973@gmail.com', [cd['email']], fail_silently=False)
            self.request.session['token'] = token
            models.Otp.objects.create(username=cd['username'], email=cd['email'], password=cd['password'],
                                      randcode=randcode, token=token)
            return redirect('account_app:check_otp')


class CheckOtpView(View):
    def get(self, request):
        if not self.request.session.get('token'):
            return redirect('account_app:register')
        form = forms.OtpForm()
        return render(request, 'account_app/otp.html', {'form': form})

    def post(self, request):
        form = forms.OtpForm(request.POST)
        if form.is_valid():
            randcode = form.cleaned_data['randcode']
            try:
                token = self.request.session.get('token')
                otp = models.Otp.objects.get(token=token,randcode=randcode)

                user = models.User.objects.create_user(email=otp.email, full_name=otp.username)
                user.set_password(otp.password)
                user.save()

                self.request.session['token'] = None
                self.request.session.modified = True
                otp.delete()

                login(request, user)
                return redirect('/')


            except:
                messages.error(request, 'please enter  code')
                return render(request, 'account_app/otp.html', {'form': form})

        messages.error(request, 'code is wrong.')
        return render(request, 'account_app/otp.html', {'form': form})


class VerifyEmailView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return render('/')
        form = forms.VerifyEmailForm()
        return render(request, 'account_app/verify_email.html', {'form': form})

    def post(self, request):
        form = forms.VerifyEmailForm(request.POST)
        if form.is_valid():
            token = str(uuid.uuid4())
            email = form.cleaned_data['email']

            user = models.User.objects.filter(email=email).first()
            if user:
                models.Profile.objects.create(email_user=email, token=token)
                send_mail('Change Password',
                          f'for change password click on link:http://127.0.0.1:8000/accounts/change/password/{token}/',
                          'rezasharafdini973@gmail.com', [email], fail_silently=False)
                messages.success(request, 'send email')
            else:
                messages.error(request, 'email valid.')
        else:
            messages.error(request, 'email ')

        return render(request, 'account_app/verify_email.html', {'form': form})


class ChangePasswordView(View):
    def get(self, request, token):
        try:
            models.Profile.objects.get(token=token)
            form = forms.ChangePasswordForm()
            return render(request, 'account_app/change_password.html', {'form': form})
        except:
            raise Http404('page not found.')

    def post(self, request, token):
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirmation_password = form.cleaned_data['confirmation_password']

            try:

                profile = models.Profile.objects.get(token=token)
                if password != confirmation_password:
                    messages.error('password and confirmation password is not same.')
                    return render(request, 'account_app/change_password.html', {'form': form})

                user = models.User.objects.get(email=profile.email_user)
                profile.delete()

                user.set_password(password)
                user.save()
                return redirect('account_app:login')
            except:
                raise Http404('page not found.')

        messages.error(request, 'please again enter password')
        return render(request, 'account_app/change_password.html', {'form': form})
