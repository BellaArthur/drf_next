from rest_framework import serializers
from django.utils import timezone
from .models import Category, Tag, Post, Comment, Like


# ─── Category ────────────────────────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


# ─── Tag ─────────────────────────────────────────────────────────────────────

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


# ─── Post List (lightweight) ─────────────────────────────────────────────────

class PostListSerializer(serializers.ModelSerializer):
    author   = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    tags     = serializers.StringRelatedField(many=True)
    likes_count    = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category',
            'tags', 'cover_image', 'status',
            'likes_count', 'comments_count', 'published_at',
        ]


# ─── Post Detail (full) ──────────────────────────────────────────────────────

class PostDetailSerializer(serializers.ModelSerializer):
    author   = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags     = TagSerializer(many=True, read_only=True)
    likes_count    = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'tags',
            'body', 'cover_image', 'status',
            'likes_count', 'comments_count',
            'created_at', 'updated_at', 'published_at',
        ]


# ─── Post Write (create & update) ────────────────────────────────────────────

class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = [
            'title', 'category', 'tags',
            'body', 'cover_image', 'status',
        ]

    def validate_status(self, value):
        # Capture published_at the moment a post goes published
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        validated_data['author'] = self.context['request'].user

        if validated_data.get('status') == Post.Status.PUBLISHED:
            validated_data['published_at'] = timezone.now()

        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)

        # Set published_at only the first time status becomes published
        if (validated_data.get('status') == Post.Status.PUBLISHED
                and instance.status != Post.Status.PUBLISHED):
            validated_data['published_at'] = timezone.now()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance


# ─── Comment ─────────────────────────────────────────────────────────────────

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'author', 'body', 'created_at']
        read_only_fields = ['author', 'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['post']   = self.context['post']
        return super().create(validated_data)


# ─── Like ────────────────────────────────────────────────────────────────────

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user', 'post', 'created_at']