from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('post/', views.post_view, name='post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
