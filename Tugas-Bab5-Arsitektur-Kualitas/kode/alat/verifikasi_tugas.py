"""
verifikasi_tugas.py
===================
Pemeriksaan independen atas angka dan klaim pada dokumen Tugas Bab 5:
batas domain, titik ON/OFF, taksonomi cacat, harga tiket, dan integrasi
satuan. Skrip berhenti dengan AssertionError bila ada satu nilai yang
tidak konsisten.
"""

from __future__ import annotations

import os


# ----------------------------------------------------------------------
# Model aturan
# ----------------------------------------------------------------------
def daftar_benar(usia: int) -> bool:
    return usia >= 18


def daftar_closure_error(usia: int) -> bool:
    return usia > 18


def daftar_shift_kanan(usia: int) -> bool:
    return usia >= 19


def daftar_shift_kiri(usia: int) -> bool:
    return usia >= 17


def harga_benar(usia: int) -> int:
    return 25000 if usia < 12 else 50000


def harga_domain_bug(usia: int) -> int:
    return 25000 if usia <= 12 else 50000


def harga_komputasi_bug(usia: int) -> int:
    return 40000 if usia < 12 else 50000


def meter_ke_cm(meter: float) -> float:
    return meter * 100.0


def tulis(teks: str = "") -> None:
    print(teks)


def bagian_usia() -> None:
    tulis("1. BATAS DOMAIN USIA (aturan: usia >= 18)")
    tulis("-" * 62)
    tulis("Jenis batas : tertutup (>=), nilai 18 termasuk domain sah")
    tulis("Titik ON    : 18 (tepat di garis batas, DITERIMA)")
    tulis("Titik OFF   : 17 (tetangga terdekat di luar domain, DITOLAK)")

    assert daftar_benar(18) is True
    assert daftar_benar(17) is False
    assert daftar_benar(19) is True
    tulis("Status      : ON=18 diterima, OFF=17 ditolak -> sesuai")

    # Setiap varian cacat harus terdeteksi oleh salah satu titik uji.
    assert daftar_closure_error(18) is False      # 18 salah ditolak
    assert daftar_shift_kanan(18) is False        # 18 salah ditolak
    assert daftar_shift_kiri(17) is True          # 17 salah diterima
    tulis("Deteksi     : closure & shift kanan ditangkap ON=18,")
    tulis("              shift kiri ditangkap OFF=17")

    # Nilai jauh dari batas tidak membedakan implementasi.
    for usia in (19, 25, 40):
        assert (daftar_benar(usia) == daftar_closure_error(usia)
                == daftar_shift_kanan(usia) == daftar_shift_kiri(usia))
    tulis("Catatan     : usia 19/25/40 tidak membedakan keempat versi")
    tulis()


def bagian_tiket() -> None:
    tulis("2. HARGA TIKET (usia < 12 -> Rp25.000, selain itu Rp50.000)")
    tulis("-" * 62)
    assert harga_benar(12) == 50000
    assert harga_benar(11) == 25000
    assert harga_domain_bug(12) == 25000       # batas salah
    assert harga_domain_bug(11) == 25000
    assert harga_komputasi_bug(10) == 40000    # rumus salah
    assert harga_komputasi_bug(12) == 50000
    tulis("Domain bug  : usia 12 seharusnya 50.000, terbaca 25.000")
    tulis("Komputasi   : usia 10 seharusnya 25.000, terbaca 40.000")
    tulis("Kesimpulan  : domain bug hanya di batas; komputasi di dalam domain")
    tulis()


def bagian_integrasi() -> None:
    tulis("3. INTEGRASI SATUAN (sensor meter -> layar sentimeter)")
    tulis("-" * 62)
    assert meter_ke_cm(1.25) == 125.0
    assert f"{meter_ke_cm(1.25):.2f} cm" == "125.00 cm"
    assert f"{1.25:.2f} cm" == "1.25 cm"          # tanpa adapter salah
    tulis("Unit sensor : 1.25 m  -> LULUS")
    tulis("Unit layar  : 125.00 cm -> LULUS")
    tulis("Integrasi   : 1.25 m dibaca 1.25 cm -> GAGAL")
    tulis("Adapter     : 1.25 m x 100 = 125.00 cm -> LULUS")
    tulis()


def bagian_taksonomi() -> None:
    tulis("4. TAKSONOMI CACAT DOMAIN")
    tulis("-" * 62)
    # Closure: >= 18 vs > 18
    assert daftar_benar(18) != daftar_closure_error(18)
    # Shifted: >= 18 vs >= 19 dan >= 17
    assert daftar_benar(18) != daftar_shift_kanan(18)
    assert daftar_benar(17) != daftar_shift_kiri(17)
    # Tilted: x + y <= 10 vs 2x + y <= 10 pada titik (5,5)
    benar = (5 + 5 <= 10)
    salah = (2 * 5 + 5 <= 10)
    assert benar is True and salah is False
    tulis("Closure : >= 18 vs > 18 (operator berbeda)")
    tulis("Shifted : >= 18 vs >= 19 / >= 17 (garis bergeser)")
    tulis("Tilted  : x + y <= 10 vs 2x + y <= 10")
    tulis("          titik (5,5): benar 10 <= 10, salah 15 <= 10")
    tulis()


def main() -> int:
    tulis("LAPORAN VERIFIKASI OTOMATIS - TUGAS BAB 5")
    tulis("Arsitektur Kualitas Perangkat Lunak")
    tulis("Domain Testing & System Integration Testing")
    tulis("=" * 70)
    tulis()

    bagian_usia()
    bagian_tiket()
    bagian_integrasi()
    bagian_taksonomi()

    tulis("=" * 70)
    tulis("SEMUA PEMERIKSAAN (assert) LULUS - angka pada dokumen konsisten.")
    tulis("=" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
