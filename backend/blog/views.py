from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from core.utils import APIResponse
from .models import Category, Tag, Post, Comment, Like
from .serializers import (
    CategorySerializer, TagSerializer,
    PostListSerializer, PostDetailSerializer, PostWriteSerializer,
    CommentSerializer,
)
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly


# ─── Category ────────────────────────────────────────────────────────────────

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field       = 'slug'

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return APIResponse.success(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )
        if not serializer.is_valid():
            return APIResponse.error(
                message='Update failed',
                errors=serializer.errors
            )
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message='Category updated successfully'
        )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return APIResponse.success(message='Category deleted successfully')


# ─── Tag ─────────────────────────────────────────────────────────────────────

class TagListCreateView(generics.ListCreateAPIView):
    queryset           = Tag.objects.all()
    serializer_class   = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Tag.objects.all()
    serializer_class   = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field       = 'slug'

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return APIResponse.success(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )
        if not serializer.is_valid():
            return APIResponse.error(
                message='Update failed',
                errors=serializer.errors
            )
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message='Tag updated successfully'
        )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return APIResponse.success(message='Tag deleted successfully')


# ─── Post ────────────────────────────────────────────────────────────────────

class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['category__slug', 'tags__slug', 'status', 'author__email']
    search_fields      = ['title', 'body']
    ordering_fields    = ['published_at', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.is_author:
            return Post.objects.filter(
                Q(status=Post.Status.PUBLISHED) | Q(author=user)
            )
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostWriteSerializer
        return PostListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message='Post creation failed',
                errors=serializer.errors
            )
        post = serializer.save()
        return APIResponse.success(
            data=PostDetailSerializer(post, context={'request': request}).data,
            message='Post created successfully',
            status_code=201
        )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field       = 'slug'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.is_author:
            return Post.objects.filter(
                Q(status=Post.Status.PUBLISHED) | Q(author=user)
            )
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostWriteSerializer
        return PostDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return APIResponse.success(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )
        if not serializer.is_valid():
            return APIResponse.error(
                message='Post update failed',
                errors=serializer.errors
            )
        post = serializer.save()
        return APIResponse.success(
            data=PostDetailSerializer(post, context={'request': request}).data,
            message='Post updated successfully'
        )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return APIResponse.success(message='Post deleted successfully')


# ─── Comment ─────────────────────────────────────────────────────────────────

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class   = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post__slug=self.kwargs['slug'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post'] = generics.get_object_or_404(
            Post, slug=self.kwargs['slug']
        )
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message='Comment creation failed',
                errors=serializer.errors
            )
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message='Comment added successfully',
            status_code=201
        )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post__slug=self.kwargs['slug'])

    def get_object(self):
        comment = super().get_object()
        if self.request.method not in ['GET'] and comment.author != self.request.user:
            self.permission_denied(self.request)
        return comment

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return APIResponse.success(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )
        if not serializer.is_valid():
            return APIResponse.error(
                message='Comment update failed',
                errors=serializer.errors
            )
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message='Comment updated successfully'
        )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return APIResponse.success(message='Comment deleted successfully')


# ─── Like ────────────────────────────────────────────────────────────────────

class LikeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        post = generics.get_object_or_404(Post, slug=slug)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return APIResponse.success(message='Post unliked')
        return APIResponse.success(message='Post liked', status_code=201)