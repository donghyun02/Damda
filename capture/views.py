# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from urllib import urlopen

from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from capture.models import Folder, Tag, Bookmark


@method_decorator(csrf_exempt, name='dispatch')
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

@method_decorator(csrf_exempt, name='dispatch')
class FolderView(View):
    def get(self, request):
        data = serializers.serialize('json', Folder.objects.all().filter(owner=request.user), fields=('name', 'bookmarks'))
        jsonData = json.loads(data)
        return JsonResponse({'state': 'success', 'data': jsonData})

    def post(self, request):
        name = request.POST.get('name')
        Folder.objects.create(name=name, owner=request.user)
        return JsonResponse({'state': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class FolderDestroyView(View):
    def post(self, request):
        name = request.POST.get('name')
        folder = Folder.objects.get(name=name)
        bookmarks = folder.bookmarks.all()

        for bookmark in bookmarks:
            bookmark.delete()

        folder.delete()
        return JsonResponse({'state': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class TagView(View):
    def get(self, request):
        data = serializers.serialize('json', Tag.objects.all().filter(owner=request.user), fields=('name'))
        jsonData = json.loads(data)
        return JsonResponse({'state': 'success', 'data': jsonData})

    def post(self, request):
        name = request.POST.get('name')
        Tag.objects.create(name=name, owner=request.user)
        return JsonResponse({'state': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class TagDestroyView(View):
    def post(self, request):
        name = request.POST.get('name')
        t = Tag.objects.get(name=name)
        t.delete()

        return JsonResponse({'state': 'success'})


@method_decorator(csrf_exempt, name='dispatch')
class BookmarkView(View):
    def get(self, request):
        tags = eval(request.GET.get('tags'))
        folder = request.GET.get('folder')

        if folder is None:
            bookmarks = Bookmark.objects.filter(owner=request.user)

        else:
            bookmarks = Folder.objects.get(name=folder, owner=request.user).bookmarks

        for tag in tags:
            bookmarks = bookmarks.filter(tags__name__exact=tag)

        data = serializers.serialize('json', bookmarks)
        jsonData = json.loads(data)

        return JsonResponse({'state': 'success', 'data': jsonData})

    def post(self, request):
        folder = request.POST.get('folder')
        name = request.POST.get('name')
        url = request.POST.get('url')

        webpage = urlopen(url).read()
        soup = BeautifulSoup(webpage, "html.parser")
        imageURL = soup.find('meta', property='og:image')
        imageURL = imageURL['content'] if url else "/static/capture/images/logo.png"

        b = Bookmark.objects.create(owner=request.user, name=name, url=url, imageURL=imageURL)
        f = Folder.objects.get(name=folder)
        f.bookmarks.add(b)
        f.save()

        return JsonResponse({'state': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class ChangeNameView(View):
    def post(self, request):
        name = request.POST.get('name')
        u = User.objects.get(username=request.user)
        u.first_name = ''
        u.last_name = name
        u.save()

        return JsonResponse({'state': 'success'})
