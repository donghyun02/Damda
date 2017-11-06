# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/login.html')

@method_decorator(csrf_exempt, name='dispatch')
class Register(View):
    def get(self, request):
        return render(request, 'accounts/register.html')