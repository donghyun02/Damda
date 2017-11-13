# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
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

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')

        if password != password2:
            return JsonResponse({'success': 'false', 'error': 'password', 'message': '비밀번호가 서로 다릅니다.'})

        try:
            User.objects.get(username=username)
            return JsonResponse({'success': 'false', 'error': 'username', 'message': '이미 존재하는 이메일입니다.'})
        except:
            User.objects.create_user(username=username, password=password, last_name=lastName, first_name=firstName)
            return JsonResponse({'success': 'true', 'message': '성공적으로 만들어졌습니다.'})
