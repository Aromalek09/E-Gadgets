#pass amalk Python@123
from django.shortcuts import render,redirect

from django.views import View
from .form import LoginForm,RegForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views.generic import TemplateView,CreateView,FormView
from django.urls import reverse_lazy

# Create your views here.



class LandingView(View):
    def get(self,request):
        return render(request,'landing.html')
    
class LandingView(TemplateView):
    template_name="landing.html"

class LoginView(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'login.html',{"form":form})
    
    def post(self,request):
        form=LoginForm(data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pswd=form.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            
            if user:
                return redirect('home')
            else:
                messages.error(request,"Login Failed")
                return redirect('log')
        return render(request,"login.html",{"form":form})
    
    
class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm
    
    
    def post(self,request):
        form=LoginForm(data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pswd=form.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Login Failed")
                return redirect('log')
        return render(request,"login.html",{"form":form})
    

class RegView(View):
    def get(self,request):
        form=RegForm
        return render(request,'reg.html',{"form":form})
    
    def post(self,request):
        formdata=RegForm(data=request.POST)
        if formdata.is_valid():
            formdata.save()
            messages.success(request,"registration successfull")
            return redirect('log')
        else:
            messages.error("registration failed")
            return render(request,'reg.html',{'form':formdata})


class RegView(CreateView):
    template_name="reg.html"
    form_class=RegForm
    success_url=reverse_lazy('log')
    
    
    def form_valid(self,form):
        messages.success(self.request,"user registration completed")
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,"user registration failed")
        return super().form_invalid(form)
    
    
        
    
    
class logoutview(View):
    def get(Self,request):
        logout(request)
        return redirect('log')