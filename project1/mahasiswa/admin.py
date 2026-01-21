from django.contrib import admin
from .models import Mahasiswa
from .models import Dosen, MataKuliah

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'npm', 'email', 'nohp', 'jurusan')
    search_fields = ('nama', 'npm', 'email')
    list_filter = ('jurusan',)
    ordering = ('-id',)
    list_per_page = 25

@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    list_display = ('nama_mk', 'kode_mk', 'sks', 'semester', 'dosen_mk', 'get_mahasiswa_count')
    search_fields = ('nama_mk', 'kode_mk')
    filter_horizontal = ('mahasiswa',)
    list_filter = ('semester', 'sks', 'dosen_mk')
    
    def get_mahasiswa_count(self, obj):
        return obj.mahasiswa.count()
    get_mahasiswa_count.short_description = 'Jumlah Mahasiswa'

admin.site.register(Dosen)

