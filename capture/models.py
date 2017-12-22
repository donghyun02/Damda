# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=50)
    url = models.TextField()
    imageURL = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    folderName = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name

class Folder(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User)
    bookmarks = models.ManyToManyField(Bookmark)

    def __str__(self):
        return self.name

class Note(models.Model):
    x = models.CharField(max_length=40)
    y = models.CharField(max_length=40)
    bookmark = models.ForeignKey(Bookmark)
    text = models.TextField(default='')