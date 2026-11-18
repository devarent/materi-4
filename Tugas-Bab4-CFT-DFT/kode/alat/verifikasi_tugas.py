"""
verifikasi_tugas.py
===================
Memverifikasi seluruh angka yang dipakai dalam dokumen jawaban:
kompleksitas siklomatis, basis jalur independen, cakupan pernyataan,
cakupan cabang, kelayakan jalur, serta pasangan Definition-Use (DU).

Jalankan dari folder ini:
    python verifikasi_tugas.py
Keluaran juga disimpan ke ../hasil/laporan_verifikasi.txt
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

from cfg_engine import CFG, tampilkan
from aliran_data import AnalisisAliranData, Pernyataan

BARIS: List[str] = []


def tulis(teks: str = "") -> None:
    print(teks)
    BARIS.append(teks)


def judul(teks: str) -> None:
    tulis()
    tulis("=" * 78)
    tulis(teks)
    tulis("=" * 78)


# ======================================================================
# Model CFG setiap soal
# ======================================================================
def cfg_soal2() -> CFG:
    g = CFG("Soal 2 - nilai kelulusan", "B1", "B6")
    g.tambah_simpul("B1", "nilai = 75")
    g.tambah_simpul("B2", "if (nilai >= 60)")
    g.tambah_simpul("B3", 'cout << "Lulus"')
    g.tambah_simpul("B4", 'cout << "Tidak lulus"')
    g.tambah_simpul("B5", 'cout << "Selesai"')
    g.tambah_simpul("B6", "end")
    for a, b in [("B1", "B2"), ("B2", "B3"), ("B2", "B4"),
                 ("B3", "B5"), ("B4", "B5"), ("B5", "B6")]:
        g.tambah_sisi(a, b)
    return g


def cfg_soal3() -> CFG:
    g = CFG("Soal 3 - cakupan pernyataan & cabang", "S1", "S5")
    g.tambah_simpul("S1", "int nilai = <input>")
    g.tambah_simpul("S2", "if (nilai >= 60)")
    g.tambah_simpul("S3", 'cout << "Lulus"')
    g.tambah_simpul("S4", 'cout << "Tidak lulus"')
    g.tambah_simpul("S5", "end")
    for a, b in [("S1", "S2"), ("S2", "S3"), ("S2", "S4"),
                 ("S3", "S5"), ("S4", "S5")]:
        g.tambah_sisi(a, b)
    return g


def cfg_soal9() -> CFG:
    g = CFG("Soal 9 contoh 1 - harga & diskon", "B1", "B7")
    g.tambah_simpul("B1", "harga = <input>")
    g.tambah_simpul("B2", "diskon = 0")
    g.tambah_simpul("B3", "if (harga > 50000)")
    g.tambah_simpul("B4", "diskon = 10")
    g.tambah_simpul("B5", "total = harga - diskon")
    g.tambah_simpul("B6", "cout << total")
    g.tambah_simpul("B7", "end")
    for a, b in [("B1", "B2"), ("B2", "B3"), ("B3", "B4"), ("B3", "B5"),
                 ("B4", "B5"), ("B5", "B6"), ("B6", "B7")]:
        g.tambah_sisi(a, b)
    return g


def cfg_soal10() -> CFG:
    g = CFG("Soal 10 - aplikasi KRS", "B1", "B8")
    g.tambah_simpul("B1", "sks = 0")
    g.tambah_simpul("B2", "baca statusMahasiswa")
    g.tambah_simpul("B3", "if (statusMahasiswa == 1)")
    g.tambah_simpul("B4", "sks = 20")
    g.tambah_simpul("B5", "if (sks >= 20)")
    g.tambah_simpul("B6", "cout << \"Boleh mengambil mata kuliah\"")
    g.tambah_simpul("B7", "cout << \"Tidak boleh mengambil mata kuliah\"")
    g.tambah_simpul("B8", "end")
    for a, b in [("B1", "B2"), ("B2", "B3"), ("B3", "B4"), ("B3", "B5"),
                 ("B4", "B5"), ("B5", "B6"), ("B5", "B7"), ("B6", "B8"),
                 ("B7", "B8")]:
        g.tambah_sisi(a, b)
    return g


# ======================================================================
# 1. Kompleksitas & basis jalur
# ======================================================================
def bagian_cfg() -> None:
    judul("1. VERIFIKASI CFG, V(G), DAN BASIS JALUR INDEPENDEN")

    for pembuat in (cfg_soal2, cfg_soal3, cfg_soal9, cfg_soal10):
        g = pembuat()
        tulis(tampilkan(g))
        tulis(f"  Validasi struktur: {g.validasi() or 'OK'}")
        tulis(f"  V(G) = E - N + 2 = {g.E} - {g.N} + 2 = {g.kompleksitas()}")
        tulis(f"  Predikat + 1      = {g.jumlah_predikat()} + 1 = "
              f"{g.jumlah_predikat() + 1}")
        assert g.kompleksitas() == g.jumlah_predikat() + 1, "rumus tidak konsisten"
        assert len(g.basis_jalur()) == g.kompleksitas(), "basis jalur != V(G)"
        tulis()

    # Kasus soal 4: E = 10, N = 9
    E, N = 10, 9
    v = E - N + 2
    tulis("Kasus Soal 4 (diberikan): E = 10, N = 9, satu komponen graf")
    tulis(f"  V(G) = E - N + 2 = {E} - {N} + 2 = {v}")
    tulis(f"  Arti: {v} jalur independen -> basis path testing butuh {v} kasus uji.")
    assert v == 3


# ======================================================================
# 2. Cakupan pernyataan & cabang (Soal 3)
# ======================================================================
def bagian_cakupan() -> None:
    judul("2. VERIFIKASI STATEMENT & BRANCH COVERAGE (SOAL 3)")

    pernyataan = ["S1: nilai = <input>", "S2: if (nilai >= 60)",
                  "S3: cout << \"Lulus\"", "S4: cout << \"Tidak lulus\""]

    def eksekusi(nilai: int) -> Tuple[List[int], str]:
        """Mengembalikan indeks pernyataan yang dieksekusi dan cabang."""
        dieksekusi = [0, 1]                     # S1 dan S2 selalu dieksekusi
        if nilai >= 60:
            dieksekusi.append(2)
            cabang = "TRUE"
        else:
            dieksekusi.append(3)
            cabang = "FALSE"
        return dieksekusi, cabang

    skenario = {
        "hanya nilai 80": [80],
        "nilai 80 dan 40": [80, 40],
    }
    hasil: Dict[str, Tuple[int, int]] = {}
    for nama, kasus in skenario.items():
        semua_pernyataan = set()
        cabang = set()
        tulis(f"\nSkenario: {nama}")
        for n in kasus:
            dieksekusi, c = eksekusi(n)
            semua_pernyataan.update(dieksekusi)
            cabang.add(c)
            tulis(f"  input {n:>4} -> pernyataan {[pernyataan[i][:2] for i in dieksekusi]}"
                  f", cabang {c}")
        sc = len(semua_pernyataan) * 100.0 / 4
        bc = len(cabang) * 100.0 / 2
        hasil[nama] = (len(semua_pernyataan), len(cabang))
        tulis(f"  Statement coverage = {len(semua_pernyataan)}/4 = {sc:.0f}%")
        tulis(f"  Branch coverage    = {len(cabang)}/2 = {bc:.0f}%")

    assert hasil["hanya nilai 80"] == (3, 1)
    assert hasil["nilai 80 dan 40"] == (4, 2)
    tulis("\nKesimpulan: satu kasus uji (80) menghasilkan 75% statement coverage")
    tulis("dan 50% branch coverage; tambahan kasus uji 40 mencapai 100%/100%.")


# ======================================================================
# 3. Kelayakan jalur (Soal 5 & 10)
# ======================================================================
def bagian_kelayakan() -> None:
    judul("3. VERIFIKASI JALUR LAYAK / TIDAK LAYAK")

    tulis("Soal 5: syarat mencapai \"Proses A\" adalah x > 10 DAN x < 5")
    batas_bawah, batas_atas = 10, 5
    irisan_kosong = (batas_bawah + 1) > (batas_atas - 1)  # tidak ada bilangan bulat
    jumlah = sum(1 for x in range(-2000, 2001) if x > 10 and x < 5)
    tulis(f"  Penyisiran x pada [-2000, 2000] : {jumlah} nilai memenuhi")
    tulis(f"  Analisis interval: (10, +inf) interseksi (-inf, 5) = kosong")
    tulis(f"  Kesimpulan: jalur B1->B2->B3(true) TIDAK LAYAK (infeasible)")
    assert jumlah == 0 and irisan_kosong

    g = cfg_soal10()

    def klasifikasi(sebagai_input: bool) -> Tuple[List[List[str]], List[List[str]]]:
        """Memeriksa kelayakan tiap jalur dengan simulasi nilai."""
        layak, tidak_layak = [], []
        for jalur in g.jalur_sederhana():
            sks = 0
            ok = True
            lanjut = {jalur[i]: jalur[i + 1] for i in range(len(jalur) - 1)}
            for node in jalur:
                if node == "B4":
                    sks = 20
                if node == "B3":
                    if lanjut.get(node) == "B5":
                        # cabang false: mungkin hanya bila status bukan input
                        if not sebagai_input:
                            ok = False
                if node == "B5":
                    tujuan = lanjut.get(node)
                    if tujuan == "B6" and sks < 20:
                        ok = False
                    if tujuan == "B7" and sks >= 20:
                        ok = False
            (layak if ok else tidak_layak).append(jalur)
        return layak, tidak_layak

    tulis("Soal 10a: kode asli dengan statusMahasiswa = 1 (konstan)")
    layak, tidak_layak = klasifikasi(sebagai_input=False)
    for jalur in g.jalur_sederhana():
        tanda = "LAYAK     " if jalur in layak else "TIDAK LAYAK"
        tulis(f"  {tanda} : {' -> '.join(jalur)}")
    tulis(f"  Jumlah jalur sederhana = {len(g.jalur_sederhana())}, "
          f"layak = {len(layak)}, tidak layak = {len(tidak_layak)}")
    tulis(f"  V(G) = {g.kompleksitas()} tetapi jalur layak hanya {len(layak)}.")
    tulis("  -> V(G) adalah batas ATAS, bukan jaminan jumlah jalur yang dapat diuji.")
    assert len(layak) == 1 and len(tidak_layak) == 3

    tulis("\nSoal 10b: setelah statusMahasiswa dijadikan input (refactoring)")
    layak2, tidak_layak2 = klasifikasi(sebagai_input=True)
    for jalur in g.jalur_sederhana():
        tanda = "LAYAK     " if jalur in layak2 else "TIDAK LAYAK"
        tulis(f"  {tanda} : {' -> '.join(jalur)}")
    tulis(f"  layak = {len(layak2)}, tidak layak = {len(tidak_layak2)}; "
          f"dua kasus uji (status 1 dan 0) mencapai 100% branch coverage.")
    assert len(layak2) == 2 and len(tidak_layak2) == 2


# ======================================================================
# 4. Analisis aliran data (Soal 8, 9, 10)
# ======================================================================
def bagian_aliran_data() -> None:
    judul("4. ANALISIS ALIRAN DATA: PASANGAN DU & ANOMALI")

    # ---- Soal 8: nilai = 70; nilai = 85; cout << nilai -------------
    g8 = CFG("Soal 8 - dead assignment", "B1", "B5")
    g8.tambah_simpul("B1", "int nilai;")
    g8.tambah_simpul("B2", "nilai = 70")
    g8.tambah_simpul("B3", "nilai = 85")
    g8.tambah_simpul("B4", "cout << nilai")
    g8.tambah_simpul("B5", "end")
    for a, b in [("B1", "B2"), ("B2", "B3"), ("B3", "B4"), ("B4", "B5")]:
        g8.tambah_sisi(a, b)
    p8 = [
        Pernyataan("B1", "deklarasi int nilai;"),
        Pernyataan("B2", "nilai = 70", tulis=("nilai",)),
        Pernyataan("B3", "nilai = 85", tulis=("nilai",)),
        Pernyataan("B4", "cout << nilai", baca=(("nilai", "c"),)),
        Pernyataan("B5", "end"),
    ]
    a8 = AnalisisAliranData(g8, p8)
    h8 = a8.jalankan()
    tulis("Soal 8 - kode: int nilai; nilai = 70; nilai = 85; cout << nilai;")
    tulis(AnalisisAliranData.ringkas(h8))
    tulis("  Kesimpulan: keluaran 85; definisi 70 adalah dead store (DDU).")
    assert len(h8.pasangan) == 1
    assert [d for d, _v in h8.def_tanpa_use] == ["B2"]

    # ---- Soal 9 contoh 1: harga / diskon ---------------------------
    g9 = cfg_soal9()
    p9 = [
        Pernyataan("B1", "harga = <input>", tulis=("harga",)),
        Pernyataan("B2", "diskon = 0", tulis=("diskon",)),
        Pernyataan("B3", "if (harga > 50000)", baca=(("harga", "p"),)),
        Pernyataan("B4", "diskon = 10", tulis=("diskon",)),
        Pernyataan("B5", "total = harga - diskon",
                   baca=(("harga", "c"), ("diskon", "c")), tulis=("total",)),
        Pernyataan("B6", "cout << total", baca=(("total", "c"),)),
        Pernyataan("B7", "end"),
    ]
    a9 = AnalisisAliranData(g9, p9)
    h9 = a9.jalankan()
    tulis("\nSoal 9 contoh 1 - kode: harga/diskon dengan cabang if")
    tulis(AnalisisAliranData.ringkas(h9))
    tulis("  Kriteria (terpenuhi/total): " + str(a9.evaluasi_kriteria(h9)))
    tulis("  Catatan: (d2 -> u3) hanya terpenuhi pada jalur FALSE,")
    tulis("           (d3 -> u3) hanya pada jalur TRUE -> All-Uses butuh 2 kasus uji.")
    assert len(h9.pasangan) == 5

    # ---- Soal 10: KRS ---------------------------------------------
    g10 = cfg_soal10()
    p10 = [
        Pernyataan("B1", "sks = 0", tulis=("sks",)),
        Pernyataan("B2", "baca statusMahasiswa", tulis=("statusMahasiswa",)),
        Pernyataan("B3", "if (statusMahasiswa == 1)",
                   baca=(("statusMahasiswa", "p"),)),
        Pernyataan("B4", "sks = 20", tulis=("sks",)),
        Pernyataan("B5", "if (sks >= 20)", baca=(("sks", "p"),)),
        Pernyataan("B6", "cout << \"Boleh ...\""),
        Pernyataan("B7", "cout << \"Tidak boleh ...\""),
        Pernyataan("B8", "end"),
    ]
    a10 = AnalisisAliranData(g10, p10)
    h10 = a10.jalankan()
    tulis("\nSoal 10 - kode KRS (statusMahasiswa sebagai input)")
    tulis(AnalisisAliranData.ringkas(h10))
    tulis("  Catatan: pada jalur mahasiswa aktif, definisi sks = 0 (B1)")
    tulis("           langsung ditimpa sks = 20 (B4) -> dead store lokal (DDU).")
    tulis("           statusMahasiswa hanya punya 1 definisi (B2), 1 p-use (B3).")
    assert ("B1", "B5", "sks") in h10.pasangan
    assert ("B4", "B5", "sks") in h10.pasangan


def main() -> int:
    tulis("LAPORAN VERIFIKASI OTOMATIS - TUGAS BAB 4 (CFT & DFT)")
    tulis("Dihasilkan oleh kode/alat/verifikasi_tugas.py")
    bagian_cfg()
    bagian_cakupan()
    bagian_kelayakan()
    bagian_aliran_data()
    tulis()
    tulis("=" * 78)
    tulis("SEMUA PEMERIKSAAN (assert) LULUS - angka pada dokumen konsisten.")
    tulis("=" * 78)

    tujuan = os.path.join(os.path.dirname(__file__), "..", "hasil",
                          "laporan_verifikasi.txt")
    with open(tujuan, "w", encoding="utf-8") as f:
        f.write("\n".join(BARIS) + "\n")
    print(f"\n[OK] Laporan disimpan: {os.path.abspath(tujuan)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
