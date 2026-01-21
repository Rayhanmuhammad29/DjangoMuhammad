from django import forms
from .models import Mahasiswa, Dosen, MataKuliah


class MahasiswaForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nama', 'npm', 'email', 'jurusan', 'nohp']

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap'}),
            'npm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan NPM'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan email'}),
            'jurusan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan jurusan'}),
            'nohp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nomor HP'}),
        }


class DosenForm(forms.ModelForm):
    class Meta:
        model = Dosen
        fields = '__all__'
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap'}),
            'nidn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan NIDN'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan email'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nomor HP'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Masukkan alamat'}),
            'homebase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan homebase/departemen'}),
        }


class MataKuliahForm(forms.ModelForm):
    class Meta:
        model = MataKuliah
        fields = '__all__'
        widgets = {
            'nama_mk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama mata kuliah'}),
            'kode_mk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan kode mata kuliah'}),
            'sks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan SKS', 'type': 'number'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan semester', 'type': 'number'}),
            'mhs_mk': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan jumlah mahasiswa', 'type': 'number'}),
            'dosen_mk': forms.Select(attrs={'class': 'form-control'}),
            'mahasiswa': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
    
    def clean_kode_mk(self):
        kode_mk = self.cleaned_data.get('kode_mk')
        # Jika sedang edit, jangan validasi kode_mk sendiri
        if self.instance.pk:
            if MataKuliah.objects.filter(kode_mk=kode_mk).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Kode MK ini sudah terdaftar untuk mata kuliah lain!")
        return kode_mk
