from django.contrib.auth.models import User
from rest_framework import serializers

from capture.models import Folder, Bookmark, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')

class TagSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ('id', 'name', 'owner')

class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Bookmark
        fields = ('id', 'owner', 'name', 'url', 'imageURL', 'tags', 'folderName')

class FolderSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    bookmarks = BookmarkSerializer(read_only=True, many=True)

    class Meta:
        model = Folder
        fields = ('id', 'name', 'owner', 'bookmarks')