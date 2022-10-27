from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('posts/', views.post_search_view, name='post_search_view'),
    path('posts/create/', views.post_create_view, name='post_create_view'),
    path('posts/<int:id>/', views.post_detail_view, name='post_detail_view'),
]
