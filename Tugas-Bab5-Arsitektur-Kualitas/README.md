# Tugas Bab 5 — Arsitektur Kualitas Perangkat Lunak

**Nama:** Muhammad Arya Fatthurahman  
**NIM:** 2023230006  
**Program Studi:** Teknologi Informasi  
**Mata Kuliah:** Software Quality Assurance (SQA)

Folder ini berisi jawaban sepuluh soal esai Bab 5 tentang **Arsitektur
Kualitas Perangkat Lunak**, dengan dua pokok bahasan yang saling melengkapi:
**Domain Testing** (pengujian batas ruang input) dan **System Integration
Testing** (pengujian kerja sama antar komponen). Setiap jawaban dilengkapi
tabel pembanding, contoh kasus, gambar, pembahasan, serta demonstrasi program
C++ yang benar-benar dikompilasi dan dijalankan.

## Berkas utama

| Berkas | Keterangan |
|---|---|
| `dokumen/Tugas_Bab5_Arsitektur_Kualitas.docx` | Dokumen tugas versi Word (siap dikumpulkan) |
| `dokumen/Tugas_Bab5_Arsitektur_Kualitas.pdf`  | Dokumen tugas versi PDF |
| `dokumen/isi_tugas.md`            | Sumber tunggal seluruh isi dokumen |
| `kode/`                           | Dua program demo C++ + alat verifikasi Python |
| `kode/hasil/laporan_eksekusi.txt` | Bukti eksekusi seluruh skenario |
| `kode/hasil/laporan_verifikasi.txt` | Ringkasan pemeriksaan angka oleh alat |

## Struktur folder

```text
Tugas-Bab5-Arsitektur-Kualitas/
├── README.md
├── dokumen/
│   ├── isi_tugas.md          sumber isi (Markdown)
│   ├── mdparse.py            parser Markdown
│   ├── md2docx.py            pembangkit Word
│   ├── md2pdf.py             pembangkit PDF
│   ├── buat_gambar.py        pembangkit gambar domain & integrasi
│   ├── gambar/               4 gambar PNG (200 dpi)
│   ├── Tugas_Bab5_Arsitektur_Kualitas.docx
│   └── Tugas_Bab5_Arsitektur_Kualitas.pdf
└── kode/
    ├── domain_demo.cpp       demo batas ON/OFF, closure, shifted, cacat komputasi
    ├── integrasi_demo.cpp    demo Unit Testing vs Integration Testing + adapter
    ├── jalankan_semua.ps1    kompilasi + eksekusi + verifikasi
    ├── alat/
    │   └── verifikasi_tugas.py  pemeriksaan otomatis seluruh angka
    ├── build/                berkas executable hasil kompilasi
    └── hasil/                keluaran program + laporan
```

## Prasyarat

- **g++** dengan dukungan C++17 (diuji dengan g++ 16.2.0, MinGW-w64).
  Pastikan `g++` dapat dipanggil dari `PATH`.
- **Python 3.10+** (diuji dengan Python 3.15) dengan paket:
  `python-docx`, `reportlab`, `matplotlib`, `Pillow`, `PyMuPDF`.
  Untuk sekadar menjalankan kode C++ dan verifikasi angka, hanya Python
  standar yang dibutuhkan.
- **PowerShell** (Windows) untuk `jalankan_semua.ps1`.

## Cara menjalankan kode

Dari folder `kode/`:

```powershell
powershell -ExecutionPolicy Bypass -File .\jalankan_semua.ps1
```

Skrip akan:
1. mengompilasi kedua program dengan `-std=c++17 -Wall -Wextra`;
2. menjalankan demo domain dan demo integrasi;
3. menjalankan verifikasi Python (`alat/verifikasi_tugas.py`);
4. menyusun `hasil/laporan_eksekusi.txt`.

Menjalankan satu program secara manual:

```powershell
g++ -std=c++17 -Wall -Wextra -O0 -o build\domain_demo domain_demo.cpp
.\build\domain_demo

g++ -std=c++17 -Wall -Wextra -O0 -o build\integrasi_demo integrasi_demo.cpp
.\build\integrasi_demo
```

## Membangun ulang dokumen

Dari folder `dokumen/`:

```powershell
python buat_gambar.py     # gambar domain & strategi integrasi
python md2docx.py         # Tugas_Bab5_Arsitektur_Kualitas.docx
python md2pdf.py          # Tugas_Bab5_Arsitektur_Kualitas.pdf
```

Word dan PDF dibangun dari `isi_tugas.md` yang sama, sehingga isinya identik.
Gambar beresolusi 200 dpi. Nama, NIM, dan program studi pada sampul diatur di
`md2docx.py` dan `md2pdf.py` (fungsi `halaman_sampul`).

## Ringkasan hasil

| Soal | Pokok bahasan | Hasil kunci |
|---|---|---|
| 1 | CFT vs Domain Testing | CFT memeriksa alur kendali; Domain Testing memeriksa batas ruang input |
| 2 | Computation bug vs domain bug | Cacat domain muncul di batas (usia 12); cacat komputasi di dalam domain (usia 10–11) |
| 3 | Batas usia ≥ 18 | Batas tertutup; ON = 18 diterima, OFF = 17 ditolak |
| 4 | Taksonomi cacat domain | Closure (`> 18`), shifted (`>= 19` / `>= 17`), tilted (`2x + y <= 10`) |
| 5 | Pentingnya integration testing | Unit sensor dan layar lulus, integrasi tanpa adapter gagal (1,25 m dibaca 1,25 cm) |
| 6 | Top-Down vs Bottom-Up | Top-Down memakai stub; Bottom-Up memakai driver |
| 7 | Komponen COTS | Risiko utama pada kontrak API, versi, format data, dan ketergantungan vendor |
| 8 | Entry & Exit Criteria | Gerbang objektif sebelum dan sesudah pengujian integrasi |
| 9 | Big-Bang | Semua modul digabung sekaligus; isolasi kegagalan sangat sulit |
| 10 | Domain Testing vs BVA | BVA adalah bentuk sederhana Domain Testing satu dimensi |

Seluruh angka di atas diperiksa ulang oleh `kode/alat/verifikasi_tugas.py`.
Skrip tersebut berhenti dengan galat (`assert`) bila ada satu angka yang tidak
konsisten, sehingga dokumen dan kode tidak dapat “berbeda cerita”.

## Catatan

- Jika muncul pesan `running scripts is disabled`, gunakan
  `powershell -ExecutionPolicy Bypass -File .\jalankan_semua.ps1`.
- Jika `g++` tidak dikenali, tambahkan folder `bin` MinGW ke `PATH`.
- Berkas di `kode/build/` dan `kode/hasil/` dapat dibuat ulang kapan saja;
  keduanya bukan sumber, melainkan bukti eksekusi.
