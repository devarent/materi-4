"""
buat_gambar.py
==============
Membuat seluruh gambar (CFG, DFG, diagram alur metodologi, peta kriteria)
untuk dokumen jawaban Tugas Bab 4.

Jalankan:  python buat_gambar.py
Keluaran:  ./gambar/*.png (200 dpi)
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

# ----------------------------------------------------------------------
# Gaya umum
# ----------------------------------------------------------------------
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 9

BIRU = "#1f4e79"
BIRU_MUDA = "#dbe8f4"
ORANYE = "#c55a11"
ORANYE_MUDA = "#fbe4d5"
HIJAU = "#375623"
HIJAU_MUDA = "#e2efda"
ABU = "#595959"
MERAH = "#c00000"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gambar")
os.makedirs(OUT, exist_ok=True)


# ----------------------------------------------------------------------
# Helper menggambar simpul dan sisi
# ----------------------------------------------------------------------
def kotak(ax, x, y, teks, w=2.3, h=0.95, warna=BIRU, isi=BIRU_MUDA,
          ukuran=9, tebal=1.4, lengkung=0.12):
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={lengkung}",
        linewidth=tebal, edgecolor=warna, facecolor=isi, zorder=2,
    )
    ax.add_patch(patch)
    ax.text(x, y, teks, ha="center", va="center", fontsize=ukuran,
            color="#111111", zorder=3, linespacing=1.35)
    return patch


def belah_ketupat(ax, x, y, teks, w=2.7, h=1.35, warna=ORANYE,
                  isi=ORANYE_MUDA, ukuran=9):
    titik = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
    ax.add_patch(Polygon(titik, closed=True, linewidth=1.5, edgecolor=warna,
                         facecolor=isi, zorder=2))
    ax.text(x, y, teks, ha="center", va="center", fontsize=ukuran,
            color="#111111", zorder=3, linespacing=1.25)


def terminal(ax, x, y, teks, w=2.2, h=0.72, warna=HIJAU, isi=HIJAU_MUDA):
    """Terminator berbentuk kapsul (mulai / selesai)."""
    kotak(ax, x, y, teks, w=w, h=h, warna=warna, isi=isi, ukuran=9,
          tebal=1.5, lengkung=h / 2 - 0.02)


def panah(ax, a: Tuple[float, float], b: Tuple[float, float],
          label: str | None = None, posisi: float = 0.5, geser=(0, 0),
          warna=ABU, putus=False, lebar=1.3, ukuran=8, rad=0.0):
    ax.add_patch(FancyArrowPatch(
        a, b, arrowstyle="-|>", mutation_scale=12, linewidth=lebar,
        color=warna, shrinkA=2, shrinkB=2, zorder=1,
        linestyle=(0, (4, 3)) if putus else "solid",
        connectionstyle=f"arc3,rad={rad}",
    ))
    if label:
        px = a[0] + (b[0] - a[0]) * posisi + geser[0]
        py = a[1] + (b[1] - a[1]) * posisi + geser[1]
        ax.text(px, py, label, fontsize=ukuran, color=warna, ha="center",
                va="center", zorder=4,
                bbox=dict(boxstyle="round,pad=0.16", facecolor="white",
                          edgecolor="none", alpha=0.92))


def siapkan_kanvas(tinggi=9.6, lebar=6.4, judul=None, subjudul=None):
    fig, ax = plt.subplots(figsize=(lebar, tinggi))
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(-0.4, tinggi - 0.4)
    ax.axis("off")
    if judul:
        ax.text(0, tinggi - 0.75, judul, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=BIRU)
    if subjudul:
        ax.text(0, tinggi - 1.12, subjudul, ha="center", va="center",
                fontsize=9, color=ABU, style="italic")
    return fig, ax


def simpan(fig, nama: str):
    jalur = os.path.join(OUT, nama)
    fig.savefig(jalur, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  [OK] gambar/{nama}")


# ======================================================================
# 1. Diagram alur metodologi pengerjaan
# ======================================================================
def gambar_metodologi():
    fig, ax = siapkan_kanvas(10.0, 7.2, "Alur Kerja Pengujian Struktural",
                             "Dari kode sumber sampai laporan cakupan")
    langkah = [
        ("1", "Kode sumber", "pahami percabangan, perulangan, dan variabel"),
        ("2", "Control Flow Graph", "simpul = blok pernyataan, sisi = alur kendali"),
        ("3", "V(G) dan basis path", "V(G) = E - N + 2 jalur independen"),
        ("4", "Rancang kasus uji", "vektor input untuk setiap jalur/kondisi"),
        ("5", "Eksekusi dan bandingkan", "hasil aktual vs hasil yang diharapkan"),
        ("6", "Ukur cakupan", "statement, branch, path, dan DU-path"),
    ]
    y = 7.9
    for nomor, judul, ket in langkah:
        kotak(ax, -0.75, y, "", w=4.8, h=1.02)
        ax.text(-2.75, y + 0.18, f"{nomor}.  {judul}", ha="left", va="center",
                fontsize=10, color=BIRU, fontweight="bold", zorder=3)
        ax.text(-2.75, y - 0.24, ket, ha="left", va="center", fontsize=7.8,
                color=ABU, zorder=3)
        y -= 1.28

    for i in range(5):
        atas = 7.9 - i * 1.28 - 0.51
        bawah = 7.9 - (i + 1) * 1.28 + 0.51
        panah(ax, (-0.75, atas), (-0.75, bawah))

    ax.text(0, 0.55, "CFT menjawab: jalur mana yang dilalui?     "
                     "DFT menjawab: di mana data didefinisikan dan digunakan?",
            ha="center", va="center", fontsize=9, color=BIRU,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#eef3f9",
                      edgecolor="#b6cbe4"))
    simpan(fig, "alur_metodologi.png")


# ======================================================================
# 2. CFG Soal 2
# ======================================================================
def gambar_cfg_soal2():
    fig, ax = siapkan_kanvas(9.6, 6.2, "CFG Soal 2 - Nilai Kelulusan",
                             "N = 6, E = 6, V(G) = 6 - 6 + 2 = 2")
    terminal(ax, 0, 7.6, "B1  nilai = 75", w=2.7)
    belah_ketupat(ax, 0, 6.25, "B2  nilai >= 60 ?", w=3.1, h=1.3)
    kotak(ax, -2.35, 4.65, 'B3  "Lulus"', w=2.1, h=0.9)
    kotak(ax, 2.35, 4.65, 'B4  "Tidak lulus"', w=2.1, h=0.9)
    kotak(ax, 0, 3.25, 'B5  "Selesai"', w=2.2, h=0.9)
    terminal(ax, 0, 1.85, "B6  end", w=1.7)

    panah(ax, (0, 7.22), (0, 6.90))
    panah(ax, (-0.95, 5.85), (-2.05, 5.12), "T (true)", posisi=0.45,
          geser=(-0.35, 0.08), warna=HIJAU)
    panah(ax, (0.95, 5.85), (2.05, 5.12), "F (false)", posisi=0.45,
          geser=(0.35, 0.08), warna=MERAH)
    panah(ax, (-2.35, 4.20), (-0.55, 3.70))
    panah(ax, (2.35, 4.20), (0.55, 3.70))
    panah(ax, (0, 2.80), (0, 2.23))

    ax.text(-3.5, 6.25, "keputusan\n(predikat)", fontsize=8, color=ORANYE,
            ha="center", va="center")
    ax.text(1.15, 2.95, "merge", fontsize=8, color=ABU, ha="left")
    ax.text(-3.55, 1.55, "2 jalur independen:\nP1 = B1-B2-B3-B5-B6\n"
                         "P2 = B1-B2-B4-B5-B6", fontsize=8.2, color=BIRU,
            ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.32", facecolor="#eef3f9",
                      edgecolor="#b6cbe4"))
    simpan(fig, "cfg_soal02.png")


# ======================================================================
# 3. CFG Soal 4 (kasus E=10, N=9)
# ======================================================================
def gambar_cfg_soal4():
    fig, ax = siapkan_kanvas(10.0, 6.8,
                             "CFG Kasus Soal 4 - Dua Keputusan Berurutan",
                             "N = 9, E = 10, V(G) = 10 - 9 + 2 = 3")
    terminal(ax, 0, 8.0, "1  mulai", w=1.9)
    belah_ketupat(ax, 0, 6.7, "2  kondisi A ?", w=3.0, h=1.3)
    kotak(ax, -2.7, 5.15, "3  blok then A", w=2.2, h=0.85)
    belah_ketupat(ax, -2.7, 3.7, "4  kondisi B ?", w=2.9, h=1.2, ukuran=8.5)
    kotak(ax, -3.8, 2.1, "5  then B", w=1.4, h=0.8, ukuran=8.5)
    kotak(ax, -1.55, 2.1, "6  merge B", w=1.85, h=0.8, ukuran=8.5)
    kotak(ax, 2.7, 5.15, "7  else A", w=1.9, h=0.85)
    kotak(ax, 0.75, 2.1, "8  merge A", w=1.9, h=0.85)
    terminal(ax, 0.75, 0.65, "9  end", w=1.7)

    panah(ax, (0, 7.62), (0, 7.28))
    panah(ax, (-1.05, 6.3), (-2.3, 5.55), "T", posisi=0.5, geser=(-0.15, 0.1),
          warna=HIJAU)
    panah(ax, (1.05, 6.3), (2.3, 5.55), "F", posisi=0.5, geser=(0.15, 0.1),
          warna=MERAH)
    panah(ax, (-2.7, 4.72), (-2.7, 4.32))
    panah(ax, (-3.35, 3.28), (-3.7, 2.52), "T", posisi=0.5,
          geser=(-0.18, 0.05), warna=HIJAU)
    panah(ax, (-1.95, 3.28), (-1.75, 2.52), "F", posisi=0.5,
          geser=(0.22, 0.05), warna=MERAH)
    panah(ax, (-3.08, 2.1), (-2.48, 2.1))
    panah(ax, (-0.62, 2.1), (-0.2, 2.1))
    panah(ax, (2.7, 4.72), (1.15, 2.53))
    panah(ax, (0.75, 1.68), (0.75, 1.03))

    ax.text(-3.95, 6.7, "predikat 1", fontsize=7.8, color=ORANYE,
            ha="center", va="center")
    ax.text(0, 0.05, "V(G) = 3  →  tiga jalur independen:  P1 = 1-2-3-4-5-6-8-9,  "
                     "P2 = 1-2-3-4-6-8-9,  P3 = 1-2-7-8-9",
            fontsize=7.8, color=BIRU, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#eef3f9",
                      edgecolor="#b6cbe4"))
    simpan(fig, "cfg_soal04.png")


# ======================================================================
# 4. CFG Soal 10 (KRS)
# ======================================================================
def gambar_cfg_soal10():
    fig, ax = siapkan_kanvas(10.4, 6.6, "CFG Soal 10 - Aplikasi KRS",
                             "N = 8, E = 9, V(G) = 9 - 8 + 2 = 3")
    terminal(ax, 0, 8.2, "B1  sks = 0", w=2.4)
    kotak(ax, 0, 7.1, "B2  baca statusMahasiswa", w=3.3, h=0.85)
    belah_ketupat(ax, 0, 5.65, "B3  status == 1 ?", w=3.2, h=1.3)
    kotak(ax, -2.55, 3.95, "B4  sks = 20", w=2.0, h=0.85)
    belah_ketupat(ax, 0, 3.95, "B5  sks >= 20 ?", w=2.9, h=1.3, ukuran=8.6)
    kotak(ax, -2.3, 2.3, 'B6  "Boleh mengambil\nmata kuliah"', w=2.5, h=1.1,
          ukuran=8)
    kotak(ax, 2.3, 2.3, 'B7  "Tidak boleh\nmengambil mata kuliah"', w=2.7,
          h=1.1, ukuran=8)
    terminal(ax, 0, 0.9, "B8  end", w=1.7)

    panah(ax, (0, 7.82), (0, 7.54))
    panah(ax, (0, 6.65), (0, 6.31))
    panah(ax, (-1.15, 5.25), (-2.25, 4.38), "T", posisi=0.5,
          geser=(-0.12, 0.1), warna=HIJAU)
    panah(ax, (1.15, 5.25), (0.72, 4.45), "F", posisi=0.55,
          geser=(0.25, 0.02), warna=MERAH, putus=True)
    panah(ax, (-1.55, 3.95), (-0.95, 3.95))
    panah(ax, (-1.25, 3.5), (-2.05, 2.9), "T", posisi=0.45,
          geser=(-0.18, 0.05), warna=HIJAU)
    panah(ax, (1.25, 3.5), (2.05, 2.9), "F", posisi=0.45,
          geser=(0.18, 0.05), warna=MERAH)
    panah(ax, (-2.3, 1.72), (-0.55, 1.18))
    panah(ax, (2.3, 1.72), (0.55, 1.18))

    ax.text(1.55, 5.75, "✗ tidak layak\n(status selalu 1)", fontsize=7.4,
            color=MERAH, ha="left", va="center")

    ax.text(0, 0.1, "Kode asli (status = 1): hanya 1 jalur layak, yaitu "
                    "B1-B2-B3-B4-B5-B6-B8.", fontsize=8, color=BIRU,
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#eef3f9",
                      edgecolor="#b6cbe4"))
    simpan(fig, "cfg_soal10.png")


# ======================================================================
# 5. DFG Soal 9 (matriks variabel x pernyataan)
# ======================================================================
def gambar_dfg_soal9():
    fig, ax = siapkan_kanvas(8.8, 7.4, "Graf Aliran Data (DFG) - Soal 9",
                             "Definisi (D) dan penggunaan (U) setiap variabel")
    lane = {"harga": -0.5, "diskon": 1.7, "total": 3.5}
    baris = [
        ("B1", "harga = <input>", 6.3),
        ("B2", "diskon = 0", 5.45),
        ("B3", "if (harga > 50000)", 4.6),
        ("B4", "diskon = 10", 3.75),
        ("B5", "total = harga - diskon", 2.9),
        ("B6", "cout << total", 2.05),
    ]
    for var, x in lane.items():
        ax.plot([x, x], [1.7, 6.75], color="#cccccc", lw=1.0, zorder=0)
        ax.text(x, 6.55, var, ha="center", va="bottom", fontsize=9.5,
                color=BIRU, fontweight="bold")
    for kode, teks, y in baris:
        ax.plot([-4.5, 4.35], [y, y], color="#efefef", lw=0.8, zorder=0)
        ax.text(-4.45, y, f"{kode}  {teks}", ha="left", va="center",
                fontsize=8, color="#333333")
        ax.plot([-2.05, -2.05], [1.7, 6.75], color="#eeeeee", lw=0.8, zorder=0)

    def titik(var, y, label, jenis):
        x = lane[var]
        warna = BIRU if jenis == "D" else ORANYE
        isi = BIRU_MUDA if jenis == "D" else ORANYE_MUDA
        ax.add_patch(plt.Circle((x, y), 0.27, facecolor=isi, edgecolor=warna,
                                lw=1.4, zorder=3))
        ax.text(x, y, label, ha="center", va="center", fontsize=7.2,
                color=warna, fontweight="bold", zorder=4)

    titik("harga", 6.3, "d1", "D")
    titik("harga", 4.6, "u1", "U")
    titik("harga", 2.9, "u2", "U")
    titik("diskon", 5.45, "d2", "D")
    titik("diskon", 3.75, "d3", "D")
    titik("diskon", 2.9, "u3", "U")
    titik("total", 2.9, "d4", "D")
    titik("total", 2.05, "u4", "U")

    def busur(var, y1, y2, rad, putus=False):
        x = lane[var]
        ax.add_patch(FancyArrowPatch(
            (x, y1 - 0.27 if y1 > y2 else y1 + 0.27),
            (x, y2 + 0.27 if y1 > y2 else y2 - 0.27),
            connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
            mutation_scale=10, lw=1.2, color=ORANYE,
            linestyle=(0, (4, 2)) if putus else "solid", zorder=2,
        ))

    busur("harga", 6.3, 4.6, 0.28)
    busur("harga", 6.3, 2.9, 0.45)
    busur("diskon", 5.45, 2.9, 0.30, putus=True)
    busur("diskon", 3.75, 2.9, -0.25)
    busur("total", 2.9, 2.05, 0.25)

    ax.text(0, 1.15, "D = definisi, U = penggunaan (p-use bila di kondisi, "
                     "c-use bila di perhitungan)\n"
                     "d1→u1, d1→u2, d2→u3 (hanya cabang FALSE), d3→u3 "
                     "(hanya cabang TRUE), d4→u4",
            ha="center", va="center", fontsize=7.8, color=ABU,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor="#dddddd"))
    simpan(fig, "dfg_soal09.png")


# ======================================================================
# 6. DFG Soal 10
# ======================================================================
def gambar_dfg_soal10():
    fig, ax = siapkan_kanvas(7.0, 6.2, "Graf Aliran Data (DFG) - Soal 10 (KRS)",
                             "Siklus hidup variabel sks dan statusMahasiswa")
    lane = {"statusMahasiswa": -1.15, "sks": 1.55}
    baris = [
        ("B1", "sks = 0", 4.5),
        ("B2", "status = input", 3.75),
        ("B3", "if (status == 1)", 3.0),
        ("B4", "sks = 20", 2.25),
        ("B5", "if (sks >= 20)", 1.5),
    ]
    for var, x in lane.items():
        ax.plot([x, x], [1.1, 4.95], color="#cccccc", lw=1.0, zorder=0)
        ax.text(x, 4.85, var, ha="center", va="bottom", fontsize=9.5,
                color=BIRU, fontweight="bold")
    for kode, teks, y in baris:
        ax.plot([-4.5, 4.35], [y, y], color="#efefef", lw=0.8, zorder=0)
        ax.text(-4.45, y, f"{kode}  {teks}", ha="left", va="center",
                fontsize=8, color="#333333")
        ax.plot([-2.35, -2.35], [1.1, 4.95], color="#eeeeee", lw=0.8,
                zorder=0)

    def titik(var, y, label, jenis):
        x = lane[var]
        warna = BIRU if jenis == "D" else ORANYE
        isi = BIRU_MUDA if jenis == "D" else ORANYE_MUDA
        ax.add_patch(plt.Circle((x, y), 0.25, facecolor=isi, edgecolor=warna,
                                lw=1.4, zorder=3))
        ax.text(x, y, label, ha="center", va="center", fontsize=7,
                color=warna, fontweight="bold", zorder=4)

    titik("sks", 4.5, "d1", "D")
    titik("sks", 2.25, "d2", "D")
    titik("sks", 1.5, "u1", "U")
    titik("statusMahasiswa", 3.75, "d3", "D")
    titik("statusMahasiswa", 3.0, "u2", "U")

    def busur(x, y1, y2, rad, warna=ORANYE, putus=False):
        ax.add_patch(FancyArrowPatch(
            (x, y1 - 0.25), (x, y2 + 0.25),
            connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
            mutation_scale=10, lw=1.2, color=warna,
            linestyle=(0, (4, 2)) if putus else "solid", zorder=2))

    busur(lane["sks"], 4.5, 1.5, -0.35, warna=MERAH, putus=True)
    busur(lane["sks"], 2.25, 1.5, 0.25)
    busur(lane["statusMahasiswa"], 3.75, 3.0, 0.25)

    ax.text(0, 0.45, "d1→u1 hanya terpenuhi bila cabang B4 tidak dilewati; "
                     "d2→u1 dan d3→u2 selalu terpenuhi.\n"
                     "Pada jalur mahasiswa aktif, d1 (sks = 0) di-kill oleh "
                     "d2 sebelum sempat dipakai (dead store / DDU).",
            ha="center", va="center", fontsize=7.8, color=ABU,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor="#dddddd"))
    simpan(fig, "dfg_soal10.png")

# ======================================================================
# 7. Peta hierarki kriteria DFT
# ======================================================================
def gambar_hierarki_kriteria():
    fig, ax = siapkan_kanvas(8.6, 6.0, "Hierarki Kriteria Cakupan Aliran Data",
                             "Kriteria di atas menuntut lebih banyak daripada "
                             "kriteria di bawah")
    kotak(ax, 0, 6.05, "All-DU-Paths\n(paling menuntut)", w=3.5, h=1.15,
          warna=BIRU, isi="#c9dcf0", ukuran=9)
    kotak(ax, 0, 4.6, "All-Uses", w=3.0, h=0.85, ukuran=9)
    kotak(ax, -1.7, 3.15, "All-C-Uses /\nSome-P-Uses", w=2.6, h=1.0,
          ukuran=8.2)
    kotak(ax, 1.7, 3.15, "All-P-Uses /\nSome-C-Uses", w=2.6, h=1.0,
          ukuran=8.2)
    kotak(ax, 0, 1.65, "All-Defs\n(paling longgar)", w=3.0, h=1.0, ukuran=9,
          warna=HIJAU, isi=HIJAU_MUDA)

    panah(ax, (-0.9, 5.55), (-0.45, 5.02), warna=ABU)
    panah(ax, (0.9, 5.55), (0.45, 5.02), warna=ABU)
    panah(ax, (-0.9, 4.18), (-1.4, 3.65), warna=ABU)
    panah(ax, (0.9, 4.18), (1.4, 3.65), warna=ABU)
    panah(ax, (-1.7, 2.65), (-0.55, 2.15), warna=ABU)
    panah(ax, (1.7, 2.65), (0.55, 2.15), warna=ABU)

    ax.text(-3.85, 4.6, "setiap definisi\n→ minimal 1 use", fontsize=7.8,
            color=ABU, ha="left", va="center")
    ax.text(3.85, 4.6, "setiap pasangan\ndef-use layak", fontsize=7.8,
            color=ABU, ha="right", va="center")
    ax.text(0, 0.55, "Catatan: hubungan inklusi bergantung pada definisi formal "
                     "kriteria dan asumsi jalur layak.",
            ha="center", va="center", fontsize=7.6, color=ABU, style="italic")
    simpan(fig, "hierarki_kriteria.png")


if __name__ == "__main__":
    print("Membuat gambar...")
    gambar_metodologi()
    gambar_cfg_soal2()
    gambar_cfg_soal4()
    gambar_cfg_soal10()
    gambar_dfg_soal9()
    gambar_dfg_soal10()
    gambar_hierarki_kriteria()
    print("Selesai.")
