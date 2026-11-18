"""
aliran_data.py
==============
Analisis aliran data (Data Flow Testing) sederhana di atas CFG:
menelusuri seluruh jalur layak, mencatat definisi (def) dan penggunaan
(use: p-use / c-use), lalu membentuk pasangan Definition-Use (DU pair).

Kriteria yang dihitung:
  - All-Defs     : setiap definisi mencapai minimal satu penggunaan.
  - All-Uses     : setiap pasangan (def, use) yang layak tercakup.
  - All-DU-Paths : setiap jalur def->use yang layak tercakup.

Anomali yang dilaporkan:
  - use-before-def : variabel dibaca sebelum ada definisi.
  - def-without-use: definisi tidak pernah mencapai penggunaan (dead store).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from cfg_engine import CFG


@dataclass
class Pernyataan:
    """Isi satu simpul CFG dari sudut pandang data."""

    node: str
    teks: str
    baca: Tuple[Tuple[str, str], ...] = ()   # ((variabel, "p"/"c"), ...)
    tulis: Tuple[str, ...] = ()              # variabel yang didefinisikan


@dataclass
class HasilAliranData:
    pasangan: Dict[Tuple[str, str, str], Set[Tuple[str, ...]]] = field(
        default_factory=dict
    )   # (def_node, use_node, var) -> himpunan jalur (sebagai tuple)
    use_tanpa_def: List[Tuple[Tuple[str, ...], str, str]] = field(default_factory=list)
    def_tanpa_use: List[Tuple[str, str]] = field(default_factory=list)
    jalur_dianalisis: int = 0


class AnalisisAliranData:
    def __init__(self, cfg: CFG, pernyataan: Sequence[Pernyataan]):
        self.cfg = cfg
        self.info: Dict[str, Pernyataan] = {p.node: p for p in pernyataan}
        hilang = set(cfg.simpul) - set(self.info)
        if hilang:
            raise ValueError(f"Simpul tanpa informasi data: {sorted(hilang)}")

    # ------------------------------------------------------------------
    def jalankan(self, saring_jalur=None) -> HasilAliranData:
        hasil = HasilAliranData()
        semua_def: Dict[str, Set[str]] = {}

        for jalur in self.cfg.jalur_sederhana():
            if saring_jalur and not saring_jalur(jalur):
                continue
            hasil.jalur_dianalisis += 1
            definisi_terakhir: Dict[str, str] = {}
            posisi = {node: i for i, node in enumerate(jalur)}

            for node in jalur:
                info = self.info[node]
                for var, jenis in info.baca:
                    if var in definisi_terakhir:
                        kunci = (definisi_terakhir[var], node, var)
                        # DU-path = subjalur dari definisi sampai penggunaan.
                        subjalur = tuple(
                            jalur[posisi[definisi_terakhir[var]]: posisi[node] + 1]
                        )
                        hasil.pasangan.setdefault(kunci, set()).add(subjalur)
                    else:
                        hasil.use_tanpa_def.append((tuple(jalur), node, var))
                for var in info.tulis:
                    definisi_terakhir[var] = node
                    semua_def.setdefault(var, set()).add(node)

        # Definisi yang tidak pernah muncul pada pasangan mana pun.
        def_terpakai = {(d, var) for (d, _u, var) in hasil.pasangan}
        for var, nodes in semua_def.items():
            for d in nodes:
                if (d, var) not in def_terpakai:
                    hasil.def_tanpa_use.append((d, var))
        return hasil

    # ------------------------------------------------------------------
    @staticmethod
    def ringkas(hasil: HasilAliranData) -> str:
        baris: List[str] = []
        baris.append(f"Jalur dianalisis : {hasil.jalur_dianalisis}")
        baris.append(f"Pasangan DU      : {len(hasil.pasangan)}")
        for (d, u, var), jalur in sorted(hasil.pasangan.items()):
            jalur_unik = {" -> ".join(j) for j in jalur}
            baris.append(
                f"  ({d} -> {u}) var '{var}' : {len(jalur_unik)} jalur unik"
            )
        if hasil.use_tanpa_def:
            baris.append("Anomali use-before-def:")
            for jalur, node, var in hasil.use_tanpa_def:
                baris.append(f"  {var} dibaca di {node} pada jalur {' -> '.join(jalur)}")
        if hasil.def_tanpa_use:
            baris.append("Anomali def-without-use (dead store):")
            for d, var in hasil.def_tanpa_use:
                baris.append(f"  definisi {var} di {d} tidak pernah digunakan")
        return "\n".join(baris)

    # ------------------------------------------------------------------
    def evaluasi_kriteria(self, hasil: HasilAliranData) -> Dict[str, Tuple[int, int]]:
        """Mengembalikan {kriteria: (terpenuhi, total)}."""
        defs = {d for (d, _u, _v) in hasil.pasangan}
        defs |= {d for (d, _v) in hasil.def_tanpa_use}
        return {
            "All-Defs": (len(defs - {d for d, _v in hasil.def_tanpa_use}), len(defs)),
            "All-Uses": (len(hasil.pasangan), len(hasil.pasangan)),
            "All-DU-Paths": (
                len({(d, u, v, j) for (d, u, v), js in hasil.pasangan.items() for j in js}),
                len({(d, u, v, j) for (d, u, v), js in hasil.pasangan.items() for j in js}),
            ),
        }
