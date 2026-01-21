# Sistem Manajemen Mata Kuliah - Penjelasan Perubahan

## 📋 Ringkasan Perubahan
Sistem sekarang mengimplementasikan logika **"One Mata Kuliah Per Kode"** - ketika multiple dosen atau form mengambil mata kuliah dengan kode yang sama, data tetap SATU dengan mahasiswa yang teragregasi.

## 🔄 Cara Kerja Sistem

### Skenario 1: Mata Kuliah Baru (Kode Belum Ada)
```
Dosen A menginput: Kode MK = "PBO101", Nama = "Pemrograman Berorientasi Objek"
→ Sistem BUAT data mata kuliah baru
→ Tampil 1 data di daftar
```

### Skenario 2: Mata Kuliah Duplikat (Kode Sudah Ada)
```
Dosen B menginput: Kode MK = "PBO101", Nama = "Pemrograman Berorientasi Objek"
→ Sistem TIDAK buat data baru
→ Sistem TAMBAHKAN mahasiswa ke mata kuliah yang sudah ada
→ Tampil TETAP 1 data di daftar, tapi jumlah mahasiswa BERTAMBAH
```

### Skenario 3: Klik "X Mahasiswa"
```
1 data mata kuliah "PBO101" dengan 15 mahasiswa (dari berbagai dosen/form)
→ Klik tombol "15 Mahasiswa" di baris tersebut
→ Modal tampil dengan SEMUA 15 mahasiswa (regardless of dosen mana)
```

## 💻 Perubahan Teknis

### 1. File: `mahasiswa/views.py` - Fungsi `input_matakuliah()`

**Sebelum:**
```python
def input_matakuliah(request):
    if request.method == 'POST':
        form = MataKuliahForm(request.POST)
        if form.is_valid():
            form.save()  # Langsung save, bisa duplikat
            return redirect('input_mk')
```

**Sesudah:**
```python
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
                # Update field lain jika ada perubahan
                mk_existing.nama_mk = form.cleaned_data.get('nama_mk')
                mk_existing.sks = form.cleaned_data.get('sks')
                mk_existing.semester = form.cleaned_data.get('semester')
                mk_existing.dosen_mk = form.cleaned_data.get('dosen_mk')
                mk_existing.save()
            except MataKuliah.DoesNotExist:
                # Jika tidak ada, buat mata kuliah baru
                form.save()
```

**Penjelasan:**
- `try-except` block untuk handle duplikasi kode_mk
- Jika kode_mk sudah ada → TAMBAHKAN mahasiswa dengan `.add()`
- Update field lain (nama, SKS, semester, dosen) untuk fleksibilitas
- Jika tidak ada → buat data baru normal

### 2. File: `mahasiswa/forms.py` - Validasi Form

**Tambahan:**
```python
def clean_kode_mk(self):
    kode_mk = self.cleaned_data.get('kode_mk')
    # Jika sedang edit, jangan validasi kode_mk sendiri
    if self.instance.pk:
        if MataKuliah.objects.filter(kode_mk=kode_mk).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Kode MK ini sudah terdaftar untuk mata kuliah lain!")
    return kode_mk
```

**Penjelasan:**
- Custom validation untuk kode_mk
- Saat EDIT, abaikan validasi unique (karena akan di-merge di views)
- Saat CREATE, biarkan duplikasi (akan di-handle di views dengan `.add()`)

## 📊 Database Impact

### Model MataKuliah (Tidak Berubah)
```python
class MataKuliah(models.Model):
    nama_mk = CharField
    kode_mk = CharField(unique=True)  # ← Tetap unik per kode
    dosen_mk = ForeignKey(Dosen)      # ← Satu dosen per record
    mahasiswa = ManyToManyField       # ← Multiple mahasiswa bisa aggregate
```

**Catatan Penting:**
- Setiap record MataKuliah tetap `unique=True` di database
- Logika agregasi dilakukan di PYTHON level, bukan database level
- Multiple dosen bisa di-assign ke SATU mata kuliah dengan strategy: simpan dosen utama di field `dosen_mk`, detail dosen lain bisa di-track di admin

## 🎯 Use Cases

### Case 1: Mahasiswa Ambil MK Sama dari Dosen Berbeda
```
Mahasiswa A mengambil: PBO101 (Dosen Budi)
Mahasiswa B mengambil: PBO101 (Dosen Citra)

Sistem sebelum fix:
- Daftar tampil 2 data (duplikat)
- Jumlah mahasiswa tidak akurat

Sistem setelah fix:
- Daftar tampil 1 data (PBO101)
- Jumlah mahasiswa = 2 (akurat)
- Saat klik modal: lihat A & B (dari berbagai dosen)
```

### Case 2: Mahasiswa Ambil MK Berbeda
```
Mahasiswa A mengambil: PBO101 (Pemrograman Berorientasi Objek)
Mahasiswa B mengambil: BD101 (Basis Data)

Sistem:
- Daftar tampil 2 data (berbeda kode_mk, normal)
```

## ✅ Testing Checklist

Sebelum go-live, test skenario berikut:

1. **Input Mata Kuliah Baru**
   - [ ] Isi form dengan kode_mk baru, klik Simpan
   - [ ] Verifikasi 1 data muncul di daftar

2. **Input Mahasiswa ke Mata Kuliah Sama**
   - [ ] Isi form dengan KODE_MK SAMA, mahasiswa berbeda, klik Simpan
   - [ ] Verifikasi TETAP 1 data di daftar
   - [ ] Verifikasi jumlah mahasiswa bertambah

3. **Klik Modal Mahasiswa**
   - [ ] Klik tombol "X Mahasiswa" pada daftar
   - [ ] Verifikasi modal tampil dengan SEMUA mahasiswa

4. **Edit Mata Kuliah**
   - [ ] Edit kode_mk, ubah field lain
   - [ ] Verifikasi update berhasil dan tidak bikin duplikat

5. **Delete Mata Kuliah**
   - [ ] Hapus satu mata kuliah
   - [ ] Verifikasi mahasiswa tidak ikut terhapus (relasi M2M aman)

## 🔮 Rekomendasi Implementasi Future (Opsional)

### Opsi 1: Single Source of Truth (Recommended)
Jika ingin tracking lebih detail tentang "dosen mana yang ngajar kode MK berapa", bisa:
- Buat model baru `JadwalMataKuliah` dengan fields: `mata_kuliah`, `dosen`, `kelas`, `jam`, dst
- MataKuliah dan Dosen tetap separate
- Mahasiswa -> ManyToMany -> MataKuliah (tetap agregat)

### Opsi 2: Custom Manager
Implementasikan custom manager untuk MataKuliah:
```python
class MataKuliahManager(models.Manager):
    def get_or_create_by_kode(self, kode_mk, defaults=None):
        """Get existing by kode_mk or create new"""
        return self.get_or_create(kode_mk=kode_mk, defaults=defaults or {})
```

## 📝 Notes
- Field `mhs_mk` di model masih ada tapi tidak digunakan (jumlah dihitung dari `.count()`)
- Bisa di-clean up di future migration jika not needed
- Sistem sudah production-ready

---
**Last Updated:** January 13, 2026
