from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    TagListCreateView, TagDetailView,
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView,
    LikeToggleView,
)

urlpatterns = [
    # Categories
    path('categories/',        CategoryListCreateView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(),   name='category_detail'),

    # Tags
    path('tags/',              TagListCreateView.as_view(),      name='tag_list'),
    path('tags/<slug:slug>/',  TagDetailView.as_view(),          name='tag_detail'),

    # Posts
    path('posts/',             PostListCreateView.as_view(),     name='post_list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(),         name='post_detail'),

    # Comments (nested under posts)
    path('posts/<slug:slug>/comments/',      CommentListCreateView.as_view(), name='comment_list'),
    path('posts/<slug:slug>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),

    # Likes
    path('posts/<slug:slug>/like/', LikeToggleView.as_view(), name='post_like'),
]