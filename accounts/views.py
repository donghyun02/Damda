# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File


@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/login.html')

    def post(self, request):
        logout(request)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'success': 'false', 'error': 'user', 'message': '존재하지 않는 사용자입니다.'})
        else:
            login(request, user)
            if os.path.exists('{}/{}png'.format(settings.MEDIA_ROOT, username)):
                print('make profile')
                f = open('{}/capture/images/default.png'.format(settings.STATIC_ROOT))
                f = File(f)
                self.handle_uploaded_file(f, username, 'png')
            return JsonResponse({'success': 'true', 'message': '로그인 성공'})

    def handle_uploaded_file(self, f, fileName, extension):
        if f != None:
            with open('{}/{}.{}'.format(settings.MEDIA_ROOT, fileName, extension), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

@method_decorator(csrf_exempt, name='dispatch')
class Register(View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/register.html')

    def post(self, request):
        logout(request)
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        print('{}'.format(settings.MEDIA_ROOT))
        if password != password2:
            return JsonResponse({'success': 'false', 'error': 'password', 'message': '비밀번호가 서로 다릅니다.'})

        try:
            User.objects.get(username=username)
            return JsonResponse({'success': 'false', 'error': 'username', 'message': '이미 존재하는 이메일입니다.'})
        except:
            u = User.objects.create_user(username=username, password=password, last_name=lastName, first_name=firstName)
            f = open('{}/capture/images/default.png'.format(settings.STATIC_ROOT))
            f = File(f)
            print(type(f))
            self.handle_uploaded_file(f, u.username, 'png')
            print('test')
            return JsonResponse({'success': 'true', 'message': '성공적으로 만들어졌습니다.'})

    def handle_uploaded_file(self, f, fileName, extension):
        if f != None:
            with open('{}/{}.{}'.format(settings.MEDIA_ROOT, fileName, extension), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/accounts/login/')