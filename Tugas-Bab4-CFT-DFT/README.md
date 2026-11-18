# Tugas Bab 4 — Software Structural Testing (CFT & DFT)

**Nama:** Muhammad Arya Fatthurahman  
**NIM:** 2023230006  
**Program Studi:** Teknologi Informasi  
**Mata Kuliah:** Software Quality Assurance (SQA)

Folder ini berisi jawaban sepuluh soal esai Bab 4 tentang *Software Structural
Testing*: **Control Flow Testing (CFT)** dan **Data Flow Testing (DFT)**.
Setiap jawaban dilengkapi analisis CFG/DFG, perhitungan kompleksitas siklomatis,
perancangan kasus uji, pembahasan, serta program C++ yang benar-benar
dikompilasi dan dijalankan.

## Berkas utama

| Berkas | Keterangan |
|---|---|
| `dokumen/Tugas_Bab4_CFT_DFT.docx` | Dokumen tugas versi Word (siap dikumpulkan) |
| `dokumen/Tugas_Bab4_CFT_DFT.pdf`  | Dokumen tugas versi PDF |
| `dokumen/isi_tugas.md`            | Sumber tunggal seluruh isi dokumen |
| `kode/`                           | Delapan program C++ solusi + alat verifikasi Python |
| `kode/hasil/laporan_eksekusi.txt` | Bukti eksekusi seluruh skenario |
| `kode/hasil/laporan_verifikasi.txt` | Ringkasan pemeriksaan angka oleh alat |

## Struktur folder

```text
Tugas-Bab4-CFT-DFT/
├── README.md
├── dokumen/
│   ├── isi_tugas.md          sumber isi (Markdown)
│   ├── mdparse.py            parser Markdown
│   ├── md2docx.py            pembangkit Word
│   ├── md2pdf.py             pembangkit PDF
│   ├── buat_gambar.py        pembangkit gambar CFG/DFG
│   ├── gambar/               7 gambar PNG (200 dpi)
│   ├── Tugas_Bab4_CFT_DFT.docx
│   └── Tugas_Bab4_CFT_DFT.pdf
└── kode/
    ├── soal02_nilai.cpp
    ├── soal03_coverage.cpp
    ├── soal04_kompleksitas.cpp
    ├── soal05_infeasible.cpp
    ├── soal06_diskon.cpp
    ├── soal08_aliran_data.cpp
    ├── soal09_kriteria.cpp
    ├── soal10_krs.cpp
    ├── jalankan_semua.ps1     kompilasi + eksekusi + verifikasi
    ├── alat/
    │   ├── cfg_engine.py      CFG, V(G), jalur sederhana, basis jalur
    │   ├── aliran_data.py     analisis DU-path dan anomali data
    │   └── verifikasi_tugas.py pemeriksaan otomatis seluruh angka
    ├── build/                 berkas executable hasil kompilasi
    └── hasil/                 keluaran program + laporan
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
1. mengompilasi kedelapan program dengan `-std=c++17 -Wall -Wextra`;
2. menjalankan dua belas skenario uji;
3. menjalankan verifikasi Python (`alat/verifikasi_tugas.py`);
4. menyusun `hasil/laporan_eksekusi.txt`.

Menjalankan satu program secara manual:

```powershell
g++ -std=c++17 -Wall -Wextra -O0 -o build\soal03_coverage soal03_coverage.cpp
.\build\soal03_coverage 80          # satu kasus uji
.\build\soal03_coverage 80 40       # dua kasus uji
```

## Membangun ulang dokumen

Dari folder `dokumen/`:

```powershell
python buat_gambar.py     # gambar CFG/DFG
python md2docx.py         # Tugas_Bab4_CFT_DFT.docx
python md2pdf.py          # Tugas_Bab4_CFT_DFT.pdf
```

Word dan PDF dibangun dari `isi_tugas.md` yang sama, sehingga isinya identik.
Gambar beresolusi 200 dpi. Nama, NIM, dan program studi pada sampul diatur di
`md2docx.py` dan `md2pdf.py` (fungsi `halaman_sampul`).

## Ringkasan hasil

| Soal | Pokok bahasan | Hasil kunci |
|---|---|---|
| 1 | Konsep structural testing | Perbedaan pengujian struktural vs pengujian keluaran |
| 2 | CFG sederhana | N=6, E=6, V(G)=2; jalur 75 (lulus) dan 50 (tidak lulus) |
| 3 | Statement & branch coverage | 3/4 = 75% dan 1/2 = 50%; tambah nilai 40 → 100% |
| 4 | Kompleksitas siklomatis | V(G) = 10 − 9 + 2 = 3; tiga jalur independen |
| 5 | Jalur tak layak | `x > 10` dan `x < 5` bertentangan; irisan kosong |
| 6 | Eksekusi simbolik | Batas `totalBelanja >= 500000`; uji 500000 vs 499999 |
| 7 | Konsep DFT | Use-before-def tidak terlihat pada CFG |
| 8 | Anomali aliran data | Keluaran 85; nilai 70 adalah dead store (DDU) |
| 9 | All-Defs/All-Uses/All-DU-Paths | 4 definisi, 5 pasangan DU, 6 DU-path |
| 10 | Integrasi CFT & DFT | V(G)=3; kode asli hanya 1 jalur layak, setelah refactor 2 |

Seluruh angka di atas diperiksa ulang oleh `kode/alat/verifikasi_tugas.py`.
Skrip tersebut berhenti dengan galat (`assert`) bila ada satu angka yang tidak
konsisten, sehingga dokumen dan kode tidak dapat “berbeda cerita”.

## Catatan

- Jika muncul pesan `running scripts is disabled`, gunakan
  `powershell -ExecutionPolicy Bypass -File .\jalankan_semua.ps1`.
- Jika `g++` tidak dikenali, tambahkan folder `bin` MinGW ke `PATH`.
- Berkas di `kode/build/` dan `kode/hasil/` dapat dibuat ulang kapan saja;
  keduanya bukan sumber, melainkan bukti eksekusi.
