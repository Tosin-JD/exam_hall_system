from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from accounts.forms import StudentCreationForm, InvigilatorCreationForm

class StudentSignUpView(CreateView):
    form_class = StudentCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')  # Redirect to the login page upon successful registration

class InvigilatorSignUpView(CreateView):
    form_class = InvigilatorCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')  # Redirect to the login page upon successful registration

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('login')  # Redirect to the home page upon successful login

