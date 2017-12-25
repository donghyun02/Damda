# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from urllib2 import urlopen

from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .filters import BookmarkListFilter
from .models import Folder, Tag, Bookmark
from .serializers import FolderSerializer, TagSerializer, BookmarkSerializer


@method_decorator(csrf_exempt, name='dispatch')
class Index(View):
    def get(self, request):
        if request.user.is_authenticated():
            u = User.objects.get(username=request.user)
            print(u.username)
            return render(request, 'capture/index.html', {'user': request.user})
        else:
            return HttpResponseRedirect('/accounts/login/')

class FolderListCreateView(generics.ListCreateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_fields = ('owner__username', 'name')

class FolderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def destroy(self, request, *args, **kwargs):
        print(request.data.get('name'))
        try:
            name = request.data.get('name')
            f = Folder.objects.get(name=name)
            for i in f.bookmarks.all():
                i.delete()
        except:
            pass
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

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

        pk = serializer.data['id']
        folderName = request.POST.get('folderName')
        check = request.POST.get('check')
        url = request.POST.get('url')

        bookmark = Bookmark.objects.get(pk=pk)
        bookmark.imageURL = self.getMetaImage(url)
        if check == 'true':
            os.system("xvfb-run python capture.py {} {}".format(request.POST.get('url'), pk))
            bookmark.url = "http://35.166.12.115:4000/app/capture/{}".format(pk)
        bookmark.save()

        folder = Folder.objects.get(name=folderName, owner__username=request.user)
        folder.bookmarks.add(bookmark)
        folder.save()

        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def getMetaImage(self, url):
        try:
            try:
                urlopen(url)
                webpage = urlopen(url).read()
                soup = BeautifulSoup(webpage, "html.parser")
                imageURL = soup.find('meta', property='og:image')
                imageURL = imageURL['content'] if url else "/static/capture/images/bookmark.png"
            except:
                try:
                    url = 'http://' + url
                    webpage = urlopen(url).read()
                    soup = BeautifulSoup(webpage, "html.parser")
                    imageURL = soup.find('meta', property='og:image')
                    imageURL = imageURL['content'] if url else "/static/capture/images/bookmark.png"
                except:
                    imageURL = "/static/capture/images/bookmark.png"
        except:
            imageURL = "/static/capture/images/bookmark.png"
        return imageURL

class BookmarkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        try:
            folder = Folder.objects.get(name=instance.folderName, owner__username=request.user)
            folder.bookmarks.remove(instance)
            folder.save()
        except:
            pass

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        try:
            folderName = request.data.get('folderName')
            print(folderName)
            folder = Folder.objects.get(owner__username=request.user, name=folderName)
            folder.bookmarks.add(instance)
            folder.save()

        except:
            pass

        try:
            tagName = request.data.get('tag')
            tag = Tag.objects.get(owner__username=request.user, name=tagName)
            instance.tags.add(tag)
            instance.save()
        except:
            pass

        return Response(serializer.data)

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
        print(request.FILES)
        image = request.FILES.get('image')
        self.handle_uploaded_file(image, request.user, 'png')
        return JsonResponse({'state': 'success'})

    def handle_uploaded_file(self, f, fileName, extension):
        if f != None:
            with open('{}/{}.{}'.format(settings.MEDIA_ROOT, fileName, extension), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

class CaptureView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        b = Bookmark.objects.get(pk=pk)
        print(b)
        image = '/static/capture/images/{}.png'.format(pk)
        return render(request, 'capture/test.html', {'image': image})