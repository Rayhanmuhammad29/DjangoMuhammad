from django.urls import path
from . import views
from .views import input_dosen, input_matakuliah, edit_dosen, delete_dosen, edit_matakuliah, delete_matakuliah

urlpatterns = [
    path('input/', views.input_mahasiswa, name='input_mahasiswa'),
    path('edit/<int:id>/', views.edit_mahasiswa, name='edit_mahasiswa'),
    path('delete/<int:id>/', views.delete_mahasiswa, name='delete_mahasiswa'),
    path('dosen/', input_dosen, name='input_dosen'),
    path('dosen/edit/<int:id>/', edit_dosen, name='edit_dosen'),
    path('dosen/delete/<int:id>/', delete_dosen, name='delete_dosen'),
    path('matakuliah/', input_matakuliah, name='input_mk'),
    path('matakuliah/edit/<int:id>/', edit_matakuliah, name='edit_matakuliah'),
    path('matakuliah/delete/<int:id>/', delete_matakuliah, name='delete_matakuliah'),
]
