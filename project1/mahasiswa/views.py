from django.shortcuts import render, redirect, get_object_or_404
from .models import Mahasiswa, Dosen, MataKuliah
from django.contrib.auth.decorators import login_required
from .forms import MahasiswaForm, DosenForm, MataKuliahForm


@login_required(login_url='/admin/login/')
def input_mahasiswa(request):
    if request.method == 'POST':
        form = MahasiswaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('input_mahasiswa')
    else:
        form = MahasiswaForm()

    data = Mahasiswa.objects.all()
    total_mahasiswa = Mahasiswa.objects.count()
    context = {
        'form': form,
        'data': data,
        'total_mahasiswa': total_mahasiswa,
    }
    return render(request, 'mahasiswa/input.html', context)


@login_required(login_url='/admin/login/')
def edit_mahasiswa(request, id):
    mhs = get_object_or_404(Mahasiswa, id=id)

    if request.method == 'POST':
        form = MahasiswaForm(request.POST, instance=mhs)
        if form.is_valid():
            form.save()
            return redirect('input_mahasiswa')
    else:
        form = MahasiswaForm(instance=mhs)

    return render(request, 'mahasiswa/edit.html', {'form': form, 'mhs': mhs, 'edit': True})


@login_required(login_url='/admin/login/')
def delete_mahasiswa(request, id):
    mhs = get_object_or_404(Mahasiswa, id=id)
    mhs.delete()
    return redirect('input_mahasiswa')


@login_required(login_url='/admin/login/')
def input_dosen(request):
    if request.method == 'POST':
        form = DosenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('input_dosen')
    else:
        form = DosenForm()
    
    dosen_list = Dosen.objects.all()
    total_dosen = Dosen.objects.count()
    context = {
        'form': form,
        'dosen_list': dosen_list,
        'total_dosen': total_dosen,
    }
    return render(request, 'mahasiswa/dosen_form.html', context)


@login_required(login_url='/admin/login/')
def edit_dosen(request, id):
    dosen = get_object_or_404(Dosen, id=id)
    
    if request.method == 'POST':
        form = DosenForm(request.POST, instance=dosen)
        if form.is_valid():
            form.save()
            return redirect('input_dosen')
    else:
        form = DosenForm(instance=dosen)
    
    return render(request, 'mahasiswa/edit_dosen.html', {'form': form, 'dosen': dosen, 'edit': True})


@login_required(login_url='/admin/login/')
def delete_dosen(request, id):
    dosen = get_object_or_404(Dosen, id=id)
    dosen.delete()
    return redirect('input_dosen')



@login_required(login_url='/admin/login/')
def input_matakuliah(request):
    if request.method == 'POST':
        form = MataKuliahForm(request.POST)
        if form.is_valid():
            kode_mk = form.cleaned_data.get('kode_mk')
            mahasiswa_list = form.cleaned_data.get('mahasiswa')
            
            # Cek apakah kode_mk sudah ada
            try:
                mk_existing = MataKuliah.objects.get(kode_mk=kode_mk)
                # Jika ada, tambahkan mahasiswa ke mata kuliah yang sudah ada
                for mahasiswa in mahasiswa_list:
                    mk_existing.mahasiswa.add(mahasiswa)
                # Update field lain jika ada perubahan (opsional)
                mk_existing.nama_mk = form.cleaned_data.get('nama_mk')
                mk_existing.sks = form.cleaned_data.get('sks')
                mk_existing.semester = form.cleaned_data.get('semester')
                mk_existing.dosen_mk = form.cleaned_data.get('dosen_mk')
                mk_existing.save()
            except MataKuliah.DoesNotExist:
                # Jika tidak ada, buat mata kuliah baru
                form.save()
            
            return redirect('input_mk')
    else:
        form = MataKuliahForm()
    
    # Tampilkan hanya mata kuliah unik (grouped by kode_mk)
    mk_list = MataKuliah.objects.all()
    total_mk = mk_list.count()
    context = {
        'form': form,
        'mk_list': mk_list,
        'total_mk': total_mk,
    }
    return render(request, 'mahasiswa/mk_form.html', context)


@login_required(login_url='/admin/login/')
def edit_matakuliah(request, id):
    mk = get_object_or_404(MataKuliah, id=id)
    
    if request.method == 'POST':
        form = MataKuliahForm(request.POST, instance=mk)
        if form.is_valid():
            form.save()
            return redirect('input_mk')
    else:
        form = MataKuliahForm(instance=mk)
    
    return render(request, 'mahasiswa/edit_matakuliah.html', {'form': form, 'mk': mk, 'edit': True})


@login_required(login_url='/admin/login/')
def delete_matakuliah(request, id):
    mk = get_object_or_404(MataKuliah, id=id)
    mk.delete()
    return redirect('input_mk')

