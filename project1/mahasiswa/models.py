from django.db import models
class Mahasiswa(models.Model):
    nama = models.CharField(max_length=200)
    npm = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    nohp = models.CharField(max_length=20)
    jurusan = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Mahasiswa"
        verbose_name_plural = "Mahasiswas"   # atau "Mahasiswa" sesuai preferensi

    def __str__(self):
        return f"{self.nama} ({self.npm})"
    
class Dosen(models.Model):
    nama = models.CharField(max_length=100)
    nidn = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    no_hp = models.CharField(max_length=15)
    alamat = models.TextField()
    homebase = models.CharField(max_length=50)

    def __str__(self):
        return self.nama


class MataKuliah(models.Model):
    nama_mk = models.CharField(max_length=100)
    kode_mk = models.CharField(max_length=10, unique=True)
    sks = models.IntegerField()
    semester = models.IntegerField()
    mhs_mk = models.IntegerField()
    dosen_mk = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    mahasiswa = models.ManyToManyField(Mahasiswa, blank=True, related_name='matakuliah_list')

    def __str__(self):
        return self.nama_mk

