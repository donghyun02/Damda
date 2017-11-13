# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

class Index(View):
    def get(self, request):
        if request.user.is_authenticated():
            u = User.objects.get(username=request.user)
            print(u.username)
            return render(request, 'capture/index.html', {'user': request.user})
        else:
            return HttpResponseRedirect('/accounts/login/')

    def handle_uploaded_file(f, fileName, extension):
        if f != None:
            with open('{}/{}.{}'.format(settings.MEDIA_ROOT, fileName, extension), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)