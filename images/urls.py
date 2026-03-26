from django.urls import path
from .views import ImageUploadView, ImageListView, ImageSearchView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('', ImageListView.as_view(), name='image-list'),
    path('search/', ImageSearchView.as_view(), name='image-search'),
]
