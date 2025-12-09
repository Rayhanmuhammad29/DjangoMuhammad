from django.urls import path
from . import views

urlpatterns = [
    path('input/', views.input_mahasiswa, name='input_mahasiswa'),
    path('edit/<int:id>/', views.edit_mahasiswa, name='edit_mahasiswa'),
    path('delete/<int:id>/', views.delete_mahasiswa, name='delete_mahasiswa'),
]
