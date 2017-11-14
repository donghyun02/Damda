# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User)

class Bookmark(models.Model):
    name = models.CharField(max_length=50)
    url = models.TextField()
    tags = models.ManyToManyField(Tag)

class Folder(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User)
    bookmarks = models.ManyToManyField(Bookmark)