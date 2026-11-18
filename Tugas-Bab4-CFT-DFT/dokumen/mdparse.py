"""
mdparse.py
==========
Parser Markdown sederhana (subset) yang dipakai untuk membangun dokumen
DOCX dan PDF dari satu sumber isi (isi_tugas.md).

Sintaks yang didukung
---------------------
# / ## / ### / ####   judul
- item                 daftar berbutir
1. item                daftar bernomor
```lang ... ```        blok kode
| a | b |              tabel (baris pemisah |---|---|)
![alt](path)           gambar, alt dipakai sebagai keterangan
> teks                 kotak catatan
[[KAP: teks ]]         keterangan tabel/gambar (italic kecil)
[[PECAH]]              pindah halaman
[[KODE: path]]         sisipkan berkas sumber sebagai blok kode
[[AMBIL: path]]        sisipkan berkas teks (keluaran program) sebagai kode
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Blok:
    jenis: str
    isi: Any = None
    level: int = 0
    bahasa: str = ""
    lebar: Optional[float] = None


def _baca_berkas_sisipan(jalur: str, akar: str) -> str:
    kandidat = [
        os.path.join(akar, jalur),
        os.path.join(os.path.dirname(akar), jalur),
    ]
    for k in kandidat:
        if os.path.isfile(k):
            with open(k, encoding="utf-8") as f:
                return f.read().rstrip("\n")
    raise FileNotFoundError(f"Berkas sisipan tidak ditemukan: {jalur}")


def parse(jalur_md: str) -> List[Blok]:
    akar = os.path.dirname(os.path.abspath(jalur_md))
    with open(jalur_md, encoding="utf-8") as f:
        baris = f.read().splitlines()

    blok: List[Blok] = []
    i = 0
    while i < len(baris):
        b = baris[i]
        strip = b.strip()

        if not strip:
            i += 1
            continue

        # ---------------------------------------------------------- kode
        if strip.startswith("```"):
            bahasa = strip[3:].strip()
            isi: List[str] = []
            i += 1
            while i < len(baris) and not baris[i].strip().startswith("```"):
                isi.append(baris[i])
                i += 1
            i += 1
            blok.append(Blok("code", "\n".join(isi), bahasa=bahasa))
            continue

        # ------------------------------------------------------- perintah
        m = re.match(r"\[\[KODE:\s*(.+?)\s*\]\]", strip)
        if m:
            isi = _baca_berkas_sisipan(m.group(1), akar)
            ext = os.path.splitext(m.group(1))[1].lstrip(".").lower()
            bahasa = {"py": "python", "cpp": "cpp", "ps1": "powershell"}.get(ext, ext)
            blok.append(Blok("code", isi, bahasa=bahasa))
            i += 1
            continue

        m = re.match(r"\[\[AMBIL:\s*(.+?)\s*\]\]", strip)
        if m:
            isi = _baca_berkas_sisipan(m.group(1), akar)
            blok.append(Blok("code", isi, bahasa="text"))
            i += 1
            continue

        m = re.match(r"\[\[KAP:\s*(.+?)\s*\]\]", strip)
        if m:
            blok.append(Blok("caption", m.group(1)))
            i += 1
            continue

        if strip == "[[PECAH]]":
            blok.append(Blok("break"))
            i += 1
            continue

        # -------------------------------------------------------- gambar
        m = re.match(r"!\[(.*?)\]\((.*?)\)", strip)
        if m:
            alt, path = m.group(1), m.group(2).strip()
            lebar = None
            mw = re.search(r"\{width=([\d.]+)cm\}", path)
            if mw:
                lebar = float(mw.group(1))
                path = path[: mw.start()].strip()
            elif "|" in path:
                path, w = path.split("|", 1)
                try:
                    lebar = float(w)
                except ValueError:
                    pass
                path = path.strip()
            blok.append(Blok("img", os.path.join(akar, path), lebar, bahasa=alt))
            i += 1
            continue

        # -------------------------------------------------------- judul
        m = re.match(r"^(#{1,4})\s+(.*)$", strip)
        if m:
            blok.append(Blok("h", m.group(2), level=len(m.group(1))))
            i += 1
            continue

        # -------------------------------------------------------- tabel
        if strip.startswith("|"):
            kumpulan: List[str] = []
            while i < len(baris) and baris[i].strip().startswith("|"):
                kumpulan.append(baris[i].strip())
                i += 1
            if len(kumpulan) >= 2 and re.match(
                r"^\|[\s:\-|]+\|$", kumpulan[1]
            ):
                def sel(s: str) -> List[str]:
                    s = s.strip()
                    if s.startswith("|"):
                        s = s[1:]
                    if s.endswith("|"):
                        s = s[:-1]
                    return [x.strip() for x in s.split("|")]

                headers = sel(kumpulan[0])
                rows = [sel(x) for x in kumpulan[2:]]
                blok.append(Blok("table", (headers, rows)))
                continue
            # bukan tabel valid -> perlakukan sebagai paragraf
            blok.append(Blok("p", " ".join(kumpulan)))
            continue

        # -------------------------------------------------------- catatan
        if strip.startswith("> "):
            isi_note = [strip[2:]]
            i += 1
            while i < len(baris) and baris[i].strip().startswith("> "):
                isi_note.append(baris[i].strip()[2:])
                i += 1
            blok.append(Blok("note", " ".join(isi_note)))
            continue

        # ---------------------------------------------------------- daftar
        if re.match(r"^[-*]\s+", strip):
            item: List[str] = []
            while i < len(baris) and re.match(r"^[-*]\s+", baris[i].strip()):
                item.append(re.sub(r"^[-*]\s+", "", baris[i].strip()))
                i += 1
            blok.append(Blok("ul", item))
            continue

        if re.match(r"^\d+\.\s+", strip):
            item = []
            while i < len(baris) and re.match(r"^\d+\.\s+", baris[i].strip()):
                item.append(re.sub(r"^\d+\.\s+", "", baris[i].strip()))
                i += 1
            blok.append(Blok("ol", item))
            continue

        # -------------------------------------------------------- paragraf
        paragraf = [strip]
        i += 1
        while i < len(baris):
            nxt = baris[i].strip()
            if (not nxt or nxt.startswith(("#", "|", "- ", "* ", "> ", "```"))
                    or re.match(r"^\d+\.\s+", nxt)
                    or nxt.startswith("![")):
                break
            paragraf.append(nxt)
            i += 1
        blok.append(Blok("p", " ".join(paragraf)))
    return blok


INLINE = re.compile(r"(\*\*.+?\*\*|`.+?`|\*[^*]+?\*)")


def inline_bagian(teks: str) -> List[Tuple[str, str]]:
    """Memecah teks menjadi potongan (jenis, isi): biasa/tebal/miring/kode."""
    hasil: List[Tuple[str, str]] = []
    pos = 0
    for m in INLINE.finditer(teks):
        if m.start() > pos:
            hasil.append(("biasa", teks[pos:m.start()]))
        potong = m.group(0)
        if potong.startswith("**"):
            # penanda kode di dalam teks tebal tidak ditampilkan mentah
            hasil.append(("tebal", potong[2:-2].replace("`", "")))
        elif potong.startswith("`"):
            hasil.append(("kode", potong[1:-1]))
        else:
            hasil.append(("miring", potong[1:-1].replace("`", "")))
        pos = m.end()
    if pos < len(teks):
        hasil.append(("biasa", teks[pos:]))
    return hasil


def teks_bersih(teks: str) -> str:
    """Membuang penanda inline (untuk keperluan pengukuran lebar)."""
    return re.sub(r"\*\*|`|\*", "", teks)
