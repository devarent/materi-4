"""
buat_gambar.py
==============
Membuat gambar untuk dokumen Tugas Bab 5:
  1. peta_konsep.png       - peta konsep domain & integration testing
  2. domain_on_off.png     - batas tertutup/terbuka dan titik ON/OFF
  3. taksonomi_cacat.png   - closure, shifted, tilted boundary error
  4. strategi_integrasi.png- top-down (stub) vs bottom-up (driver)

Jalankan:  python buat_gambar.py
Keluaran:  ./gambar/*.png (200 dpi)
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

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
MERAH_MUDA = "#fbe5e5"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gambar")
os.makedirs(OUT, exist_ok=True)


def kotak(ax, x, y, teks, w=2.2, h=0.8, warna=BIRU, isi=BIRU_MUDA,
          ukuran=8.6, tebal=1.2, putus=False, gaya="-"):
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.10",
        linewidth=tebal, edgecolor=warna, facecolor=isi, zorder=2,
        linestyle=(0, (4, 3)) if putus else "solid",
    )
    ax.add_patch(patch)
    ax.text(x, y, teks, ha="center", va="center", fontsize=ukuran,
            color="#111111", zorder=3, linespacing=1.3)
    return patch


def panah(ax, a, b, warna=ABU, putus=False, lebar=1.2, rad=0.0,
          kepala=11):
    ax.add_patch(FancyArrowPatch(
        a, b, arrowstyle="-|>", mutation_scale=kepala, linewidth=lebar,
        color=warna, shrinkA=2, shrinkB=2, zorder=1,
        linestyle=(0, (4, 3)) if putus else "solid",
        connectionstyle=f"arc3,rad={rad}",
    ))


def simpan(fig, nama):
    jalur = os.path.join(OUT, nama)
    fig.savefig(jalur, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  [OK] gambar/{nama}")


# ======================================================================
# 1. Peta konsep
# ======================================================================
def gambar_peta_konsep():
    fig, ax = plt.subplots(figsize=(12.2, 6.4))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 6.4)
    ax.axis("off")

    ax.text(6.1, 6.02, "Peta Konsep Bab 5", ha="center", va="center",
            fontsize=15, fontweight="bold", color=BIRU)
    ax.text(6.1, 5.62, "Dua sudut pandang pengujian yang saling melengkapi",
            ha="center", va="center", fontsize=9.5, color=ABU, style="italic")

    # panel kiri
    ax.add_patch(FancyBboxPatch((0.35, 1.05), 5.45, 4.05,
                                boxstyle="round,pad=0.04,rounding_size=0.15",
                                linewidth=1.4, edgecolor=BIRU,
                                facecolor="#f7fafd", zorder=0))
    ax.text(3.07, 4.78, "DOMAIN TESTING", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=BIRU)
    ax.text(3.07, 4.42, "memeriksa kebenaran batas ruang input",
            ha="center", va="center", fontsize=8.6, color=ABU, style="italic")

    kiri = [
        ("Batas tertutup (≤, ≥)\ndan terbuka (<, >)", 3.07, 3.68),
        ("Titik ON dan OFF\ndi sekitar garis batas", 3.07, 2.95),
        ("Taksonomi cacat:\nclosure, shifted, tilted", 3.07, 2.22),
        ("BVA: perluasan uji\nnilai batas black-box", 3.07, 1.49),
    ]
    for teks, x, y in kiri:
        kotak(ax, x, y, teks, w=4.55, h=0.62, warna=BIRU,
              isi=BIRU_MUDA, ukuran=8.8)

    # panel kanan
    ax.add_patch(FancyBboxPatch((6.4, 1.05), 5.45, 4.05,
                                boxstyle="round,pad=0.04,rounding_size=0.15",
                                linewidth=1.4, edgecolor=ORANYE,
                                facecolor="#fdf8f4", zorder=0))
    ax.text(9.12, 4.78, "SYSTEM INTEGRATION TESTING",
            ha="center", va="center", fontsize=12.5, fontweight="bold",
            color=ORANYE)
    ax.text(9.12, 4.42, "memeriksa kerja sama antar komponen",
            ha="center", va="center", fontsize=8.6, color=ABU, style="italic")

    kanan = [
        ("Cacat antarmuka: tipe, satuan,\nprotokol, status global", 9.12, 3.68),
        ("Top-Down dengan stub\nBottom-Up dengan driver", 9.12, 2.95),
        ("Big-Bang, COTS, dan\nintegrasi perangkat keras", 9.12, 2.22),
        ("SIT Plan: entry dan exit\ncriteria yang terukur", 9.12, 1.49),
    ]
    for teks, x, y in kanan:
        kotak(ax, x, y, teks, w=4.55, h=0.62, warna=ORANYE,
              isi=ORANYE_MUDA, ukuran=8.8)

    # penghubung
    panah(ax, (5.35, 3.07), (6.85, 3.07), warna=HIJAU, lebar=1.8, kepala=13)
    ax.text(6.1, 3.32, "saling\nmelengkapi", ha="center", va="bottom",
            fontsize=8.2, color=HIJAU, fontweight="bold")

    ax.text(6.1, 0.52,
            "Unit Testing membuktikan komponen bekerja sendiri; "
            "Integration Testing membuktikan komponen bekerja bersama.",
            ha="center", va="center", fontsize=9, color=ABU)

    simpan(fig, "peta_konsep.png")


# ======================================================================
# 2. Titik ON dan OFF
# ======================================================================
def _garis_batas(ax, batas, kiri, kanan, valid_kanan=True):
    ax.axvline(batas, color=BIRU, linewidth=2.2, zorder=3)
    if valid_kanan:
        ax.axvspan(batas, kanan, color=HIJAU_MUDA, zorder=0)
        ax.axvspan(kiri, batas, color=MERAH_MUDA, zorder=0)
    else:
        ax.axvspan(kiri, batas, color=HIJAU_MUDA, zorder=0)
        ax.axvspan(batas, kanan, color=MERAH_MUDA, zorder=0)


def gambar_on_off():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.0, 6.2),
                                 gridspec_kw={"height_ratios": [1, 1]})
    fig.suptitle("Titik ON dan Titik OFF pada Batas Domain",
                 fontsize=14.5, fontweight="bold", color=BIRU, y=0.98)

    # --- panel atas: batas tertutup usia >= 18
    a1.set_xlim(13.5, 22.5)
    a1.set_ylim(-0.9, 1.6)
    a1.set_yticks([])
    for s in ("top", "right", "left"):
        a1.spines[s].set_visible(False)
    _garis_batas(a1, 18, 13.5, 22.5, valid_kanan=True)
    a1.set_title("Batas tertutup:  usia ≥ 18  (18 termasuk domain sah)",
                 fontsize=10.5, color=BIRU, pad=8)

    a1.plot([18], [0.62], "o", ms=13, mfc=HIJAU, mec="white", mew=2, zorder=5)
    a1.annotate("ON = 18\n(sah, tepat di batas)", xy=(18, 0.62),
                xytext=(19.6, 1.18), fontsize=9, color=HIJAU,
                ha="left", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=HIJAU, lw=1.4))
    a1.plot([17], [0.2], "o", ms=13, mfc=MERAH, mec="white", mew=2, zorder=5)
    a1.annotate("OFF = 17\n(ditolak, di luar domain)", xy=(17, 0.2),
                xytext=(14.0, 1.18), fontsize=9, color=MERAH,
                ha="left", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=MERAH, lw=1.4))
    a1.text(20.6, -0.55, "domain sah", ha="center", fontsize=8.8, color=HIJAU)
    a1.text(15.6, -0.55, "domain tidak sah", ha="center", fontsize=8.8,
            color=MERAH)
    a1.set_xticks([14, 15, 16, 17, 18, 19, 20, 21, 22])
    a1.tick_params(axis="x", labelsize=9)

    # --- panel bawah: batas terbuka suhu > 30
    a2.set_xlim(27.0, 33.0)
    a2.set_ylim(-0.9, 1.6)
    a2.set_yticks([])
    for s in ("top", "right", "left"):
        a2.spines[s].set_visible(False)
    _garis_batas(a2, 30, 27.0, 33.0, valid_kanan=True)
    a2.set_title("Batas terbuka:  suhu > 30°C  (30 tidak termasuk domain sah)",
                 fontsize=10.5, color=ORANYE, pad=8)

    a2.plot([30], [0.62], "o", ms=13, mfc=MERAH, mec="white", mew=2, zorder=5)
    a2.annotate("ON = 30\n(di luar domain)", xy=(30, 0.62),
                xytext=(28.0, 1.18), fontsize=9, color=MERAH,
                ha="left", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=MERAH, lw=1.4))
    a2.plot([31], [0.2], "o", ms=13, mfc=HIJAU, mec="white", mew=2, zorder=5)
    a2.annotate("OFF = 31\n(sah, tetangga terdekat)", xy=(31, 0.2),
                xytext=(31.4, 1.18), fontsize=9, color=HIJAU,
                ha="left", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=HIJAU, lw=1.4))
    a2.text(31.7, -0.55, "domain sah", ha="center", fontsize=8.8, color=HIJAU)
    a2.text(28.4, -0.55, "domain tidak sah", ha="center", fontsize=8.8,
            color=MERAH)
    a2.set_xticks([27, 28, 29, 30, 31, 32, 33])
    a2.tick_params(axis="x", labelsize=9)

    fig.text(0.5, 0.015,
             "Aturan modul: pada batas tertutup ON berada di dalam domain; "
             "pada batas terbuka ON berada di luar domain dan OFF di dalam.",
             ha="center", fontsize=8.6, color=ABU, style="italic")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    simpan(fig, "domain_on_off.png")


# ======================================================================
# 3. Taksonomi cacat domain (2 x 2)
# ======================================================================
def gambar_taksonomi():
    fig, axs = plt.subplots(2, 2, figsize=(11.4, 8.6))
    fig.suptitle("Tiga Taksonomi Cacat Domain",
                 fontsize=14.5, fontweight="bold", color=BIRU, y=0.985)

    # (a) batas benar
    ax = axs[0][0]
    ax.set_xlim(13, 23)
    ax.set_ylim(-0.6, 1.5)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.axvspan(18, 23, color=HIJAU_MUDA)
    ax.axvspan(13, 18, color=MERAH_MUDA)
    ax.axvline(18, color=HIJAU, linewidth=2.4)
    ax.plot([18], [0.75], "o", ms=10, mfc=HIJAU, mec="white", mew=1.6)
    ax.set_title("(a) Benar:  usia ≥ 18", fontsize=10.5, color=HIJAU, pad=6)
    ax.text(18.3, 1.12, "18 diterima", fontsize=8.8, color=HIJAU)
    ax.text(15.4, 1.12, "17 ditolak", fontsize=8.8, color=MERAH)
    ax.set_xticks([14, 16, 18, 20, 22])

    # (b) closure error
    ax = axs[0][1]
    ax.set_xlim(13, 23)
    ax.set_ylim(-0.6, 1.5)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.axvspan(18, 23, color=HIJAU_MUDA)
    ax.axvspan(13, 18, color=MERAH_MUDA)
    ax.axvline(18, color=MERAH, linewidth=2.4, linestyle="--")
    ax.plot([18], [0.75], "o", ms=10, mfc=MERAH, mec="white", mew=1.6)
    ax.set_title("(b) Closure error:  usia > 18", fontsize=10.5,
                 color=MERAH, pad=6)
    ax.text(18.3, 1.12, "18 ikut ditolak", fontsize=8.8, color=MERAH,
            fontweight="bold")
    ax.text(14.0, -0.38, "operator ≥ berubah menjadi >", fontsize=8.4,
            color=ABU, style="italic")
    ax.set_xticks([14, 16, 18, 20, 22])

    # (c) shifted boundary
    ax = axs[1][0]
    ax.set_xlim(13, 23)
    ax.set_ylim(-0.6, 1.5)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.axvspan(20, 23, color=HIJAU_MUDA)
    ax.axvspan(13, 18, color=MERAH_MUDA)
    ax.axvspan(18, 20, color="#f4b183", alpha=0.55, hatch="//")
    ax.axvline(18, color=HIJAU, linewidth=2.0, linestyle=":")
    ax.axvline(20, color=ORANYE, linewidth=2.4)
    ax.annotate("", xy=(20, 0.35), xytext=(18, 0.35),
                arrowprops=dict(arrowstyle="<|-|>", color=ORANYE, lw=1.6))
    ax.text(19.0, 0.52, "geser +2", ha="center", fontsize=8.6,
            color=ORANYE, fontweight="bold")
    ax.set_title("(c) Shifted boundary:  usia ≥ 20", fontsize=10.5,
                 color=ORANYE, pad=6)
    ax.text(14.0, -0.38, "garis batas bergeser paralel", fontsize=8.4,
            color=ABU, style="italic")
    ax.set_xticks([14, 16, 18, 20, 22])

    # (d) tilted boundary
    ax = axs[1][1]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 14)
    xs = [0, 10]
    ax.fill_between([0, 10, 0], [0, 0, 10], [0, 0, 0], color=HIJAU_MUDA,
                    alpha=0.8)
    ax.plot([0, 10], [10, 0], color=HIJAU, linewidth=2.4,
            label="benar: x + y ≤ 10")
    ax.plot([0, 5], [10, 0], color=MERAH, linewidth=2.2, linestyle="--",
            label="salah: 2x + y ≤ 10")
    ax.plot([5], [5], "o", ms=9, mfc=ORANYE, mec="white", mew=1.6, zorder=5)
    ax.annotate("(5, 5)\nbenar: 10 ≤ 10\nsalah: 15 ≤ 10", xy=(5, 5),
                xytext=(7.4, 8.4), fontsize=8.4, color=ORANYE,
                arrowprops=dict(arrowstyle="-|>", color=ORANYE, lw=1.3))
    ax.set_title("(d) Tilted boundary:  x + y ≤ 10", fontsize=10.5,
                 color=BIRU, pad=6)
    ax.set_xlabel("x", fontsize=9)
    ax.set_ylabel("y", fontsize=9)
    ax.grid(True, linestyle=":", alpha=0.45)
    ax.legend(loc="lower left", fontsize=8, frameon=True)
    ax.set_aspect("equal")

    fig.text(0.5, 0.012,
             "Closure = salah operator; shifted = garis bergeser; "
             "tilted = kemiringan/koefisien berubah.",
             ha="center", fontsize=9, color=ABU, style="italic")
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    simpan(fig, "taksonomi_cacat.png")


# ======================================================================
# 4. Top-Down vs Bottom-Up
# ======================================================================
def gambar_strategi():
    fig, (kiri, kanan) = plt.subplots(1, 2, figsize=(12.0, 6.8))
    fig.suptitle("Strategi Pengujian Integrasi", fontsize=14.5,
                 fontweight="bold", color=BIRU, y=0.98)

    for ax, judul, warna in ((kiri, "Top-Down", BIRU),
                             (kanan, "Bottom-Up", ORANYE)):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")
        ax.set_title(judul, fontsize=12.5, fontweight="bold", color=warna,
                     pad=10)

    # --- kiri: top-down
    kotak(kiri, 5, 8.4, "M1  Modul Utama", w=4.4, h=0.85, warna=BIRU,
          isi=BIRU_MUDA, ukuran=9.2)
    kotak(kiri, 2.7, 6.4, "M2", w=2.0, h=0.75, warna=BIRU, isi=BIRU_MUDA)
    kotak(kiri, 7.3, 6.4, "M3", w=2.0, h=0.75, warna=BIRU, isi=BIRU_MUDA)
    kotak(kiri, 2.7, 4.2, "S1  stub", w=2.2, h=0.75, warna=ABU,
          isi="#eeeeee", putus=True, ukuran=8.6)
    kotak(kiri, 7.3, 4.2, "S2  stub", w=2.2, h=0.75, warna=ABU,
          isi="#eeeeee", putus=True, ukuran=8.6)

    panah(kiri, (5, 7.97), (2.7, 6.78), warna=BIRU)
    panah(kiri, (5, 7.97), (7.3, 6.78), warna=BIRU)
    panah(kiri, (2.7, 6.02), (2.7, 4.58), warna=ABU, putus=True)
    panah(kiri, (7.3, 6.02), (7.3, 4.58), warna=ABU, putus=True)

    kiri.text(5, 2.75, "Arah pengujian: atas → bawah\n"
              "Modul bawah belum siap diganti STUB",
              ha="center", fontsize=8.8, color=ABU, linespacing=1.5)
    kiri.text(5, 1.55, "Kelebihan: demo alur utama cepat\n"
              "Risiko: stub tidak realistis",
              ha="center", fontsize=8.4, color=BIRU, linespacing=1.5)

    # --- kanan: bottom-up
    kotak(kanan, 2.7, 3.7, "M4", w=2.0, h=0.75, warna=ORANYE,
          isi=ORANYE_MUDA)
    kotak(kanan, 7.3, 3.7, "M5", w=2.0, h=0.75, warna=ORANYE,
          isi=ORANYE_MUDA)
    kotak(kanan, 2.7, 5.9, "M2", w=2.0, h=0.75, warna=ORANYE,
          isi=ORANYE_MUDA)
    kotak(kanan, 7.3, 5.9, "M3", w=2.0, h=0.75, warna=ORANYE,
          isi=ORANYE_MUDA)
    kotak(kanan, 5.0, 8.1, "D  driver", w=2.4, h=0.75, warna=ABU,
          isi="#eeeeee", putus=True, ukuran=8.6)

    panah(kanan, (2.7, 4.07), (2.7, 5.52), warna=ORANYE)
    panah(kanan, (7.3, 4.07), (7.3, 5.52), warna=ORANYE)
    panah(kanan, (2.7, 6.27), (4.65, 7.72), warna=ABU, putus=True)
    panah(kanan, (7.3, 6.27), (5.35, 7.72), warna=ABU, putus=True)

    kanan.text(5, 2.55, "Arah pengujian: bawah → atas\n"
               "Modul atas belum siap diganti DRIVER",
               ha="center", fontsize=8.8, color=ABU, linespacing=1.5)
    kanan.text(5, 1.35, "Kelebihan: inti sistem teruji dini\n"
               "Risiko: driver menambah pekerjaan",
               ha="center", fontsize=8.4, color=ORANYE, linespacing=1.5)

    fig.text(0.5, 0.015,
             "Stub = pengganti modul yang dipanggil (bawah); "
             "driver = pemanggil tiruan untuk modul yang diuji (atas).",
             ha="center", fontsize=8.8, color=ABU, style="italic")
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    simpan(fig, "strategi_integrasi.png")


if __name__ == "__main__":
    print("Membuat gambar Tugas Bab 5 ...")
    gambar_peta_konsep()
    gambar_on_off()
    gambar_taksonomi()
    gambar_strategi()
    print("Selesai.")
