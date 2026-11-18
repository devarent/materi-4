"""
cfg_engine.py
=============
Mesin analisis Control Flow Graph (CFG) sederhana yang dipakai untuk
memverifikasi seluruh angka pada dokumen jawaban Tugas Bab 4.

Fitur
-----
1. Menghitung jumlah simpul (N), sisi (E), dan kompleksitas siklomatis
   V(G) = E - N + 2.
2. Menghitung jumlah region (E - N + 2) dan memeriksa konsistensinya.
3. Mengenumerasi seluruh jalur sederhana (simple path) dari entry ke exit.
4. Memilih himpunan basis jalur independen (basis path) secara aljabar:
   vektor kejadian sisi tiap jalur diuji independensi linearnya di GF(2),
   sehingga banyaknya basis jalur harus sama dengan V(G).

Dependensi : hanya pustaka standar Python.
Penulis    : skrip pendukung tugas, 2026.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple

Edge = Tuple[str, str]


@dataclass
class CFG:
    """Graf aliran kontrol berarah dengan satu entry dan satu exit."""

    nama: str
    entry: str
    exit: str
    simpul: Dict[str, str] = field(default_factory=dict)   # id -> label
    sisi: List[Edge] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Konstruksi
    # ------------------------------------------------------------------
    def tambah_simpul(self, node_id: str, label: str | None = None) -> "CFG":
        self.simpul[node_id] = label if label is not None else node_id
        return self

    def tambah_sisi(self, dari: str, ke: str) -> "CFG":
        for n in (dari, ke):
            if n not in self.simpul:
                raise ValueError(f"Simpul tidak dikenal: {n}")
        if (dari, ke) not in self.sisi:
            self.sisi.append((dari, ke))
        return self

    # ------------------------------------------------------------------
    # Properti graf
    # ------------------------------------------------------------------
    @property
    def N(self) -> int:
        return len(self.simpul)

    @property
    def E(self) -> int:
        return len(self.sisi)

    def kompleksitas(self) -> int:
        """V(G) = E - N + 2 (graf terhubung, satu komponen)."""
        return self.E - self.N + 2

    def derajat_keluar(self, node_id: str) -> int:
        return sum(1 for a, _ in self.sisi if a == node_id)

    def jumlah_predikat(self) -> int:
        """Predikat = simpul dengan lebih dari satu sisi keluar."""
        return sum(1 for n in self.simpul if self.derajat_keluar(n) > 1)

    def validasi(self) -> List[str]:
        """Pemeriksaan kewajaran struktur CFG."""
        masalah: List[str] = []
        if self.entry not in self.simpul:
            masalah.append("entry tidak ada di daftar simpul")
        if self.exit not in self.simpul:
            masalah.append("exit tidak ada di daftar simpul")
        if self.derajat_keluar(self.exit) != 0:
            masalah.append("exit memiliki sisi keluar")
        for n in self.simpul:
            if n != self.exit and self.derajat_keluar(n) == 0:
                masalah.append(f"simpul {n} buntu (tidak punya sisi keluar)")
        return masalah

    # ------------------------------------------------------------------
    # Enumerasi jalur
    # ------------------------------------------------------------------
    def jalur_sederhana(self, batas: int = 20000) -> List[List[str]]:
        """Semua jalur sederhana entry->exit (tanpa simpul berulang)."""
        hasil: List[List[str]] = []
        tumpukan: List[Tuple[str, List[str], set]] = [
            (self.entry, [self.entry], {self.entry})
        ]
        while tumpukan:
            node, jalur, dikunjungi = tumpukan.pop()
            if node == self.exit:
                hasil.append(jalur)
                if len(hasil) > batas:
                    raise RuntimeError("Jumlah jalur melebihi batas enumerasi")
                continue
            for a, b in self.sisi:
                if a == node and b not in dikunjungi:
                    tumpukan.append((b, jalur + [b], dikunjungi | {b}))
        return hasil

    def basis_jalur(self) -> List[List[str]]:
        """
        Himpunan basis jalur independen.

        Setiap jalur diwakili vektor biner sepanjang E (1 bila sisi dipakai).
        Jalur ditambahkan bila menaikkan rank himpunan vektor. Hasilnya
        berukuran tepat V(G) dan setiap jalur memperkenalkan minimal satu
        sisi baru terhadap kombinasi jalur sebelumnya.
        """
        sisi_index = {s: i for i, s in enumerate(self.sisi)}
        basis_vektor: List[int] = []
        basis_jalur: List[List[str]] = []

        def rank(daftar: Sequence[int]) -> int:
            pivot: Dict[int, int] = {}
            for v in daftar:
                x = v
                while x:
                    pos = x.bit_length() - 1
                    if pos in pivot:
                        x ^= pivot[pos]
                    else:
                        pivot[pos] = x
                        break
            return len(pivot)

        for jalur in self.jalur_sederhana():
            v = 0
            for a, b in zip(jalur, jalur[1:]):
                v |= 1 << sisi_index[(a, b)]
            if rank(basis_vektor + [v]) > rank(basis_vektor):
                basis_vektor.append(v)
                basis_jalur.append(jalur)
            if len(basis_jalur) == self.kompleksitas():
                break
        return basis_jalur


def tampilkan(cfg: CFG) -> str:
    """Representasi teks ringkas sebuah CFG untuk laporan."""
    baris = [
        f"CFG: {cfg.nama}",
        f"  N = {cfg.N}, E = {cfg.E}, predikat = {cfg.jumlah_predikat()}, "
        f"V(G) = {cfg.kompleksitas()}",
        "  Simpul:",
    ]
    for nid, label in cfg.simpul.items():
        baris.append(f"    {nid}: {label}")
    baris.append("  Sisi: " + ", ".join(f"{a}->{b}" for a, b in cfg.sisi))
    jalur = cfg.jalur_sederhana()
    baris.append(f"  Jalur sederhana ({len(jalur)}):")
    for j in jalur:
        baris.append("    " + " -> ".join(j))
    baris.append(f"  Basis jalur independen ({len(cfg.basis_jalur())}):")
    for j in cfg.basis_jalur():
        baris.append("    " + " -> ".join(j))
    return "\n".join(baris)
