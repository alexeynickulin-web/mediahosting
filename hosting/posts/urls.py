from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('posts/', views.post_search_view, name='post_search_view'),
    path('posts/create/', views.post_create_view, name='post_create_view'),
    path(
        'posts/<slug:slug>/',
        views.post_detail_view,
        name='post_detail_view'
    ),
    path(
        'posts/<slug:slug>/edit/',
        views.post_update_view,
        name='post_update_view'
    ),
    path(
        'posts/<slug:slug>/delete/',
        views.post_delete_view,
        name='post_delete_view'
    ),
]
