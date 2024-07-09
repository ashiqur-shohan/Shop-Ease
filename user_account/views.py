from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.mixins import LoginRequiredMixin

#local file import
from .forms import LoginForm,UserRegistrationForm
from .mixing import LogoutRequiredMixin

###### views start  ##########


class Login(LogoutRequiredMixin,generic.View):
    # template_name = 'authentication/login.html'
    def get(self,*args,**kwargs):
        form = LoginForm()
        context = {
            'form' : form 
        }
        return render(self.request, 'authentication/login.html',context)
    def post(self,*args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            user = authenticate(
                self.request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )
            if user:
                login(self.request,user)
                return redirect('home')
            else:
                messages.error(self.request,'Wrong Credential')
                return redirect('login')
        context = {
            'form': form
        }
        return render(self.request, 'authentication/login.html',context)

class Logout(generic.View):
    def get(self,*args, **kwargs):
        logout(self.request)
        return redirect('login')
    

class Registration(generic.CreateView):
    template_name = 'authentication/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        messages.success(self.request, "Registration Successfull !")
        return super().form_valid(form)
