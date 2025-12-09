from django import forms
from .models import Mahasiswa

class MahasiswaForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nama', 'npm', 'email', 'alamat', 'jurusan', 'nohp']

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'npm': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'jurusan': forms.TextInput(attrs={'class': 'form-control'}),
            'nohp': forms.TextInput(attrs={'class': 'form-control'}),
        }
