# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from urllib import urlopen

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from capture.filters import BookmarkListFilter
from capture.models import Folder, Tag, Bookmark
from capture.serializers import FolderSerializer, TagSerializer, BookmarkSerializer


@method_decorator(csrf_exempt, name='dispatch')
class Index(View):
    def get(self, request):
        if request.user.is_authenticated():
            u = User.objects.get(username=request.user)
            print(u.username)
            return render(request, 'capture/index.html', {'user': request.user})
        else:
            return HttpResponseRedirect('/accounts/login/')

    def handle_uploaded_file(self, f, fileName, extension):
        if f != None:
            with open('{}/{}.{}'.format(settings.MEDIA_ROOT, fileName, extension), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

class FolderListCreateView(generics.ListCreateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_fields = ('owner__username', 'name')

class FolderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_fields = ('owner__username', 'name')

class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BookmarkListCreateView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    filter_class = BookmarkListFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        folderName = request.POST.get('folderName')
        pk = serializer.data['id']
        bookmark = Bookmark.objects.get(pk=pk)
        folder = Folder.objects.get(name=folderName)
        folder.bookmarks.add(bookmark)
        folder.save()

        url = request.POST.get('url')
        webpage = urlopen(url).read()
        soup = BeautifulSoup(webpage, "html.parser")
        imageURL = soup.find('meta', property='og:image')
        imageURL = imageURL['content'] if url else "/static/capture/images/logo.png"

        bookmark.imageURL = imageURL
        bookmark.save()

        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class BookmarkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ChangeNameView(View):
    def post(self, request):
        name = request.POST.get('name')
        u = User.objects.get(username=request.user)
        u.first_name = ''
        u.last_name = name
        u.save()

        return JsonResponse({'state': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class ChangeProfileImageView(View):
    def post(self, request):
        image = request.FILES.get('image')
        self.handle_uploaded_file(image, request.user, 'png')
        return JsonResponse({'state': 'success'})

    def handle_uploaded_file(self, f, fileName, extension):
        if f != None:
            with open('{}/{}.{}'.format(settings.MEDIA_ROOT, fileName, extension), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
