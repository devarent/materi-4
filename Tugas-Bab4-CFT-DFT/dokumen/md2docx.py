"""
md2docx.py
==========
Membangun dokumen Word (.docx) dari isi_tugas.md.

Jalankan:  python md2docx.py
Keluaran:  Tugas_Bab4_CFT_DFT.docx
"""

from __future__ import annotations

import os
from typing import List, Sequence

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import mdparse
from mdparse import Blok

BIRU = RGBColor(0x1F, 0x4E, 0x79)
BIRU_TERANG = RGBColor(0x2E, 0x74, 0xB5)
ABU = RGBColor(0x59, 0x59, 0x59)
HITAM = RGBColor(0x1A, 0x1A, 0x1A)

FONT_ISI = "Times New Roman"
FONT_JUDUL = "Calibri"
FONT_KODE = "Consolas"

HALAMAN_LEBAR = 21.0
MARGIN = 2.2
LEBAR_ISI_CM = HALAMAN_LEBAR - 2 * MARGIN


# ----------------------------------------------------------------------
# Utilitas XML
# ----------------------------------------------------------------------
def arsir(sel, warna: str) -> None:
    """Memberi warna latar pada sel atau paragraf."""
    tcPr = sel._tc.get_or_add_tcPr() if hasattr(sel, "_tc") else None
    target = tcPr if tcPr is not None else sel._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), warna)
    target.append(shd)


def batas_sel(sel, warna="BFBFBF", ukuran=4) -> None:
    tcPr = sel._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for sisi in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{sisi}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(ukuran))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), warna)
        borders.append(el)
    tcPr.append(borders)


def batas_paragraf(par, warna="D9D9D9", sisi="left", ukuran=12) -> None:
    pPr = par._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    el = OxmlElement(f"w:{sisi}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(ukuran))
    el.set(qn("w:space"), "6")
    el.set(qn("w:color"), warna)
    pbdr.append(el)
    pPr.append(pbdr)


def nomor_halaman(par) -> None:
    run = par.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    run._r.addnext(fld)


def spasi_baris(par, nilai=1.25, sebelum=0, sesudah=6) -> None:
    pf = par.paragraph_format
    pf.line_spacing = nilai
    pf.space_before = Pt(sebelum)
    pf.space_after = Pt(sesudah)


# ----------------------------------------------------------------------
# Teks kaya (inline)
# ----------------------------------------------------------------------
def tambah_inline(par, teks: str, ukuran: float = 11, warna=HITAM,
                  font: str = FONT_ISI) -> None:
    for jenis, isi in mdparse.inline_bagian(teks):
        if jenis == "kode":
            run = par.add_run(isi)
            run.font.name = FONT_KODE
            run.font.size = Pt(ukuran - 1)
            run.font.color.rgb = RGBColor(0x9C, 0x2A, 0x00)
        else:
            run = par.add_run(isi)
            run.font.name = font
            run.font.size = Pt(ukuran)
            run.font.color.rgb = warna
            if jenis == "tebal":
                run.bold = True
            elif jenis == "miring":
                run.italic = True


# ----------------------------------------------------------------------
# Dokumen
# ----------------------------------------------------------------------
def siapkan_dokumen() -> Document:
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(MARGIN)
    sec.right_margin = Cm(MARGIN)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(1.9)
    sec.different_first_page_header_footer = True

    gaya = doc.styles["Normal"]
    gaya.font.name = FONT_ISI
    gaya.font.size = Pt(11)
    gaya.font.color.rgb = HITAM
    gaya.paragraph_format.space_after = Pt(6)
    gaya.paragraph_format.line_spacing = 1.2
    gaya.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_ISI)

    for nama, ukuran, warna, sebelum, sesudah in [
        ("Heading 1", 17, BIRU, 18, 8),
        ("Heading 2", 13.5, BIRU_TERANG, 14, 6),
        ("Heading 3", 11.5, BIRU, 10, 4),
    ]:
        st = doc.styles[nama]
        st.font.name = FONT_JUDUL
        st.font.size = Pt(ukuran)
        st.font.bold = True
        st.font.color.rgb = warna
        st.paragraph_format.space_before = Pt(sebelum)
        st.paragraph_format.space_after = Pt(sesudah)
        st.paragraph_format.keep_with_next = True
        st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_JUDUL)

    # header (bukan halaman pertama)
    hdr = sec.header.paragraphs[0]
    hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = hdr.add_run("Tugas Bab 4  ·  Software Structural Testing (CFT & DFT)")
    run.font.name = FONT_JUDUL
    run.font.size = Pt(8.5)
    run.font.color.rgb = ABU
    batas_paragraf(hdr, warna="D6E4F0", sisi="bottom", ukuran=6)

    ftr = sec.footer.paragraphs[0]
    ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    nomor_halaman(ftr)
    for r in ftr.runs:
        r.font.name = FONT_JUDUL
        r.font.size = Pt(9)
        r.font.color.rgb = ABU

    return doc


def halaman_sampul(doc: Document) -> None:
    def kosong(n=1, ukuran=11):
        for _ in range(n):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            p.add_run(" ").font.size = Pt(ukuran)

    kosong(2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("TUGAS MATA KULIAH")
    r.font.name = FONT_JUDUL
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = ABU
    p.paragraph_format.space_after = Pt(2)
    r._element.get_or_add_rPr().append(_spasi_huruf(60))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("SOFTWARE QUALITY ASSURANCE")
    r.font.name = FONT_JUDUL
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = BIRU_TERANG
    p.paragraph_format.space_after = Pt(26)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Software Structural Testing")
    r.font.name = FONT_JUDUL
    r.font.size = Pt(29)
    r.font.bold = True
    r.font.color.rgb = BIRU
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Control Flow Testing (CFT)  &  Data Flow Testing (DFT)")
    r.font.name = FONT_JUDUL
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0xC5, 0x5A, 0x11)
    p.paragraph_format.space_after = Pt(10)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Jawaban 10 Soal Esai, Analisis CFG/DFG, Perancangan Kasus Uji,\n"
                  "dan Implementasi Program Pendukung")
    r.font.name = FONT_ISI
    r.font.size = Pt(11.5)
    r.font.italic = True
    r.font.color.rgb = ABU
    p.paragraph_format.space_after = Pt(18)

    garis = doc.add_paragraph()
    garis.alignment = WD_ALIGN_PARAGRAPH.CENTER
    batas_paragraf(garis, warna="C55A11", sisi="bottom", ukuran=12)
    garis.paragraph_format.space_after = Pt(28)

    info = [
        ("Disusun oleh", "Muhammad Arya Fatthurahman"),
        ("NIM", "2023230006"),
        ("Program Studi", "Teknologi Informasi"),
        ("Mata Kuliah", "Software Quality Assurance (SQA)"),
        ("Materi", "Bab 4 — Software Structural Testing"),
    ]
    tabel = doc.add_table(rows=0, cols=2)
    tabel.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabel.columns[0].width = Cm(4.6)
    tabel.columns[1].width = Cm(7.4)
    for k, v in info:
        sel = tabel.add_row().cells
        sel[0].width = Cm(4.6)
        sel[1].width = Cm(7.4)
        p0 = sel[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(k)
        r0.font.name = FONT_JUDUL
        r0.font.size = Pt(10)
        r0.font.color.rgb = ABU
        p1 = sel[1].paragraphs[0]
        r1 = p1.add_run(":  " + v)
        r1.font.name = FONT_ISI
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = HITAM
    kosong(4)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("2026")
    r.font.name = FONT_JUDUL
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = BIRU

    doc.add_page_break()


def _spasi_huruf(nilai: int):
    el = OxmlElement("w:spacing")
    el.set(qn("w:val"), str(nilai))
    return el


def daftar_isi(doc: Document, blok: Sequence[Blok]) -> None:
    doc.add_heading("Daftar Isi", level=1)
    p = doc.add_paragraph()
    r = p.add_run("Struktur dokumen jawaban ini:")
    r.font.size = Pt(9.5)
    r.font.italic = True
    r.font.color.rgb = ABU
    for b in blok:
        if b.jenis != "h" or b.level > 2:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0 if b.level == 1 else 0.8)
        r = p.add_run(("" if b.level == 1 else "–  ") + mdparse.teks_bersih(b.isi))
        r.font.name = FONT_JUDUL
        r.font.size = Pt(10.5 if b.level == 1 else 9.8)
        r.font.bold = b.level == 1
        r.font.color.rgb = BIRU if b.level == 1 else HITAM
    doc.add_page_break()


def judul(doc: Document, teks: str, level: int) -> None:
    h = doc.add_heading(level=level)
    r = h.add_run(mdparse.teks_bersih(teks))
    r.font.name = FONT_JUDUL


def paragraf(doc: Document, teks: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.28
    p.paragraph_format.space_after = Pt(6)
    tambah_inline(p, teks)


def butir(doc: Document, items: Sequence[str], bernomor: bool) -> None:
    for nomor, teks in enumerate(items, 1):
        if bernomor:
            # nomor ditulis manual agar setiap daftar dimulai dari 1
            # (gaya "List Number" bawaan Word melanjutkan nomor daftar sebelumnya)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.95)
            p.paragraph_format.first_line_indent = Cm(-0.55)
            p.paragraph_format.tab_stops.add_tab_stop(Cm(0.95))
            r = p.add_run(f"{nomor}.")
            r.font.name = FONT_ISI
            r.font.size = Pt(11)
            r.bold = True
            p.add_run("\t")
        else:
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.left_indent = Cm(0.9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        tambah_inline(p, teks)


def kotak_kode(doc: Document, teks: str, bahasa: str = "") -> None:
    tabel = doc.add_table(rows=1, cols=1)
    tabel.alignment = WD_TABLE_ALIGNMENT.CENTER
    sel = tabel.rows[0].cells[0]
    sel.width = Cm(LEBAR_ISI_CM)
    arsir(sel, "F7F7F5")
    batas_sel(sel, warna="E2E2DE", ukuran=4)
    p = sel.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.keep_together = True
    baris = teks.split("\n")
    for i, b in enumerate(baris):
        run = p.add_run(b.replace("\t", "    "))
        run.font.name = FONT_KODE
        run.font.size = Pt(8.2)
        run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        if i < len(baris) - 1:
            run.add_break()
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def tabel_data(doc: Document, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    lebar_kolom = _bagi_lebar(headers, rows)
    tabel = doc.add_table(rows=1, cols=len(headers))
    tabel.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabel.autofit = False
    # Word memakai w:tblGrid sebagai acuan; samakan dengan lebar tiap sel
    for i, w in enumerate(lebar_kolom):
        tabel.columns[i].width = Cm(w)
    hdr = tabel.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].width = Cm(lebar_kolom[i])
        arsir(hdr[i], "1F4E79")
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        r = p.add_run(mdparse.teks_bersih(h))
        r.font.name = FONT_JUDUL
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for idx, baris in enumerate(rows):
        sel = tabel.add_row().cells
        for i, isi in enumerate(baris):
            if i >= len(headers):
                continue
            sel[i].width = Cm(lebar_kolom[i])
            if idx % 2 == 1:
                arsir(sel[i], "F2F6FA")
            p = sel[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            tambah_inline(p, isi, ukuran=8.8, font=FONT_ISI)
    # baris header diulang antar halaman
    trPr = tabel.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _bagi_lebar(headers, rows) -> List[float]:
    """Bagi lebar kolom (cm) agar kata terpanjang tidak terpotong."""
    jumlah = len(headers)
    minimum: List[float] = []
    alami: List[float] = []
    for i in range(jumlah):
        teks_kolom = [mdparse.teks_bersih(str(headers[i]))]
        teks_kolom += [mdparse.teks_bersih(str(r[i])) for r in rows if i < len(r)]
        kata = max((len(w) for t in teks_kolom for w in t.split()), default=1)
        # perkiraan lebar huruf Times New Roman 9 pt
        minimum.append(kata * 0.172 + 0.55)
        alami.append(min(max((len(t) for t in teks_kolom), default=1) * 0.158 + 0.55,
                         9.2))
    total_min = sum(minimum)
    if total_min >= LEBAR_ISI_CM:
        skala = LEBAR_ISI_CM / total_min
        return [w * skala for w in minimum]
    sisa = LEBAR_ISI_CM - total_min
    bobot = [max(0.0, a - m) for a, m in zip(alami, minimum)]
    total_bobot = sum(bobot)
    if total_bobot <= 0:
        return [m + sisa / jumlah for m in minimum]
    return [m + sisa * b / total_bobot for m, b in zip(minimum, bobot)]


def gambar(doc: Document, path: str, lebar: float | None, keterangan: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    lebar_cm = min(lebar or 15.2, 15.8)
    p.add_run().add_picture(path, width=Cm(lebar_cm))
    if keterangan:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_after = Pt(10)
        r = cap.add_run(keterangan)
        r.font.name = FONT_ISI
        r.font.size = Pt(9)
        r.font.italic = True
        r.font.color.rgb = ABU


def catatan(doc: Document, teks: str) -> None:
    tabel = doc.add_table(rows=1, cols=1)
    tabel.alignment = WD_TABLE_ALIGNMENT.CENTER
    sel = tabel.rows[0].cells[0]
    sel.width = Cm(LEBAR_ISI_CM)
    arsir(sel, "EAF1F8")
    batas_sel(sel, warna="B6CBE4", ukuran=4)
    p = sel.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    tambah_inline(p, teks, ukuran=9.8)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def keterangan(doc: Document, teks: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(teks)
    r.font.name = FONT_ISI
    r.font.size = Pt(9)
    r.font.italic = True
    r.font.color.rgb = ABU


def bangun(berkas_md: str, tujuan: str) -> None:
    blok = mdparse.parse(berkas_md)
    doc = siapkan_dokumen()
    halaman_sampul(doc)
    daftar_isi(doc, blok)

    pertama = True
    for b in blok:
        if b.jenis == "h":
            if b.level == 1:
                if not pertama:
                    doc.add_page_break()
                pertama = False
            judul(doc, b.isi, b.level)
        elif b.jenis == "p":
            paragraf(doc, b.isi)
        elif b.jenis == "ul":
            butir(doc, b.isi, False)
        elif b.jenis == "ol":
            butir(doc, b.isi, True)
        elif b.jenis == "code":
            kotak_kode(doc, b.isi, b.bahasa)
        elif b.jenis == "table":
            headers, rows = b.isi
            tabel_data(doc, headers, rows)
        elif b.jenis == "img":
            gambar(doc, b.isi, b.level, b.bahasa)
        elif b.jenis == "note":
            catatan(doc, b.isi)
        elif b.jenis == "caption":
            keterangan(doc, b.isi)
        elif b.jenis == "break":
            doc.add_page_break()

    doc.save(tujuan)
    print(f"[OK] Word  : {tujuan}")


if __name__ == "__main__":
    akar = os.path.dirname(os.path.abspath(__file__))
    bangun(os.path.join(akar, "isi_tugas.md"),
           os.path.join(akar, "Tugas_Bab4_CFT_DFT.docx"))
