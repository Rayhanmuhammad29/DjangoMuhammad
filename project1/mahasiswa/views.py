from django.shortcuts import render, redirect, get_object_or_404
from .models import Mahasiswa
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def input_mahasiswa(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        npm = request.POST.get('npm')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        jurusan = request.POST.get('jurusan')
        nohp = request.POST.get('nohp')

        Mahasiswa.objects.create(
            nama=nama,
            npm=npm,
            email=email,
            alamat=alamat,
            jurusan=jurusan,
            nohp=nohp
        )
        return redirect('/mahasiswa/input/')

    data = Mahasiswa.objects.all()
    return render(request, 'mahasiswa/input.html', {'data': data})

@login_required(login_url='/admin/login/')
def edit_mahasiswa(request, id):
    mhs = get_object_or_404(Mahasiswa, id=id)

    if request.method == 'POST':
        mhs.nama = request.POST.get('nama')
        mhs.npm = request.POST.get('npm')
        mhs.email = request.POST.get('email')
        mhs.alamat = request.POST.get('alamat')
        mhs.jurusan = request.POST.get('jurusan')
        mhs.nohp = request.POST.get('nohp')
        mhs.save()
        return redirect('/mahasiswa/input/')

    return render(request, 'mahasiswa/edit.html', {'mhs': mhs})

@login_required(login_url='/admin/login/')
def delete_mahasiswa(request, id):
    mhs = get_object_or_404(Mahasiswa, id=id)
    mhs.delete()
    return redirect('/mahasiswa/input/')
