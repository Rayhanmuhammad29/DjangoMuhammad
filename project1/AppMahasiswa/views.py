from django.shortcuts import render
from django.http import HttpResponse
from mahasiswa.models import Mahasiswa, Dosen, MataKuliah
from django.db.models import Count, Q

def index(request):
    # Get statistics
    total_mahasiswa = Mahasiswa.objects.count()
    total_dosen = Dosen.objects.count()
    total_matakuliah = MataKuliah.objects.count()
    
    # Get data untuk chart
    mahasiswa_list = Mahasiswa.objects.all()
    dosen_list = Dosen.objects.all()
    matakuliah_list = MataKuliah.objects.all()
    
    # Count by jurusan
    jurusan_counts = {}
    for mhs in mahasiswa_list:
        jurusan = mhs.jurusan
        jurusan_counts[jurusan] = jurusan_counts.get(jurusan, 0) + 1
    
    # Count mahasiswa per mata kuliah
    mk_mhs_counts = {}
    for mk in matakuliah_list:
        mk_mhs_counts[mk.nama_mk] = mk.mhs_mk
    
    # Data untuk chart
    context = {
        'total_mahasiswa': total_mahasiswa,
        'total_dosen': total_dosen,
        'total_matakuliah': total_matakuliah,
        'mahasiswa_list': mahasiswa_list[:5],  # Latest 5
        'dosen_list': dosen_list[:5],
        'matakuliah_list': matakuliah_list[:5],
        'jurusan_counts': jurusan_counts,
        'mk_mhs_counts': mk_mhs_counts,
    }
    
    return render(request, 'AppMahasiswa/dashboard.html', context)
