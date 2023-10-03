from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views import View

from . import forms
from django.views.generic import FormView


class ContactUsView(FormView):
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
