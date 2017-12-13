# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Folder, Tag, Bookmark

admin.site.register(Folder)
admin.site.register(Tag)
admin.site.register(Bookmark)