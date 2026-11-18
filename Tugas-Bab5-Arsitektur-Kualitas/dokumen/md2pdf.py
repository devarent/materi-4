"""
md2pdf.py
=========
Membangun dokumen PDF dari isi_tugas.md menggunakan ReportLab.

Jalankan:  python md2pdf.py
Keluaran:  Tugas_Bab5_Arsitektur_Kualitas.pdf
"""

from __future__ import annotations

import os
from typing import List, Sequence

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image,
                                KeepTogether, ListFlowable, ListItem,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Preformatted, Spacer, Table,
                                TableStyle)
from reportlab.pdfbase.pdfmetrics import stringWidth

import mdparse
from mdparse import Blok

BIRU = colors.HexColor("#1F4E79")
BIRU_TERANG = colors.HexColor("#2E74B5")
ORANYE = colors.HexColor("#C55A11")
ABU = colors.HexColor("#595959")
HITAM = colors.HexColor("#1A1A1A")
LATAR_KODE = colors.HexColor("#F7F7F5")

LEBAR_HALAMAN, TINGGI_HALAMAN = A4
MARGIN_KIRI = MARGIN_KANAN = 2.2 * cm
MARGIN_ATAS = 2.0 * cm
MARGIN_BAWAH = 1.9 * cm
LEBAR_ISI = LEBAR_HALAMAN - MARGIN_KIRI - MARGIN_KANAN


# ----------------------------------------------------------------------
# Font
# ----------------------------------------------------------------------
def daftarkan_font() -> None:
    akar = os.path.dirname(os.path.abspath(__file__))
    kandidat = []
    try:
        import matplotlib
        kandidat.append(os.path.join(matplotlib.get_data_path(), "fonts", "ttf"))
    except Exception:
        pass
    kandidat += [
        r"C:\Windows\Fonts",
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
    ]

    pasangan = {
        "Isi": ("DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf",
                "DejaVuSerif-Italic.ttf", "DejaVuSerif-BoldItalic.ttf"),
        "Judul": ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf",
                  "DejaVuSans-Oblique.ttf", "DejaVuSans-BoldOblique.ttf"),
        "Kode": ("DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf",
                 "DejaVuSansMono-Oblique.ttf", "DejaVuSansMono-BoldOblique.ttf"),
    }
    for nama, berkas in pasangan.items():
        for folder in kandidat:
            jalur = [os.path.join(folder, b) for b in berkas]
            if all(os.path.isfile(j) for j in jalur):
                pdfmetrics.registerFont(TTFont(nama, jalur[0]))
                pdfmetrics.registerFont(TTFont(nama + "-Bold", jalur[1]))
                pdfmetrics.registerFont(TTFont(nama + "-Italic", jalur[2]))
                pdfmetrics.registerFont(TTFont(nama + "-BoldItalic", jalur[3]))
                pdfmetrics.registerFontFamily(
                    nama, normal=nama, bold=nama + "-Bold",
                    italic=nama + "-Italic",
                    boldItalic=nama + "-BoldItalic")
                break
        else:
            raise RuntimeError(f"Font {nama} tidak ditemukan")


# ----------------------------------------------------------------------
# Gaya paragraf
# ----------------------------------------------------------------------
def buat_gaya() -> dict:
    s = getSampleStyleSheet()
    gaya = {
        "isi": ParagraphStyle(
            "Isi", parent=s["BodyText"], fontName="Isi", fontSize=9.9,
            leading=14.4, alignment=TA_JUSTIFY, textColor=HITAM,
            spaceAfter=5.5,
        ),
        "h1": ParagraphStyle(
            "H1", fontName="Judul-Bold", fontSize=16.5, leading=21,
            textColor=BIRU, spaceBefore=6, spaceAfter=9,
        ),
        "h2": ParagraphStyle(
            "H2", fontName="Judul-Bold", fontSize=12.4, leading=16,
            textColor=BIRU_TERANG, spaceBefore=12, spaceAfter=5,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3", fontName="Judul-Bold", fontSize=10.6, leading=14,
            textColor=BIRU, spaceBefore=8, spaceAfter=3,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "H4", fontName="Judul-Bold", fontSize=9.9, leading=13,
            textColor=HITAM, spaceBefore=6, spaceAfter=2,
            keepWithNext=True,
        ),
        "kode": ParagraphStyle(
            "Kode", fontName="Kode", fontSize=7.1, leading=9.1,
            textColor=colors.HexColor("#222222"),
            backColor=LATAR_KODE, borderColor=colors.HexColor("#E2E2DE"),
            borderWidth=0.5, borderPadding=(5, 6, 5, 6),
            leftIndent=0, spaceBefore=2, spaceAfter=2,
        ),
        "sel": ParagraphStyle(
            "Sel", fontName="Isi", fontSize=7.9, leading=10.2,
            textColor=HITAM, alignment=TA_LEFT,
        ),
        "sel_head": ParagraphStyle(
            "SelHead", fontName="Judul-Bold", fontSize=8.1, leading=10.4,
            textColor=colors.white, alignment=TA_CENTER,
        ),
        "caption": ParagraphStyle(
            "Caption", fontName="Isi-Italic", fontSize=8.2, leading=11,
            textColor=ABU, alignment=TA_CENTER, spaceBefore=2, spaceAfter=8,
        ),
        "note": ParagraphStyle(
            "Note", fontName="Isi", fontSize=9.2, leading=13,
            textColor=HITAM, alignment=TA_LEFT,
        ),
        "daftar": ParagraphStyle(
            "Daftar", fontName="Isi", fontSize=9.9, leading=14,
            textColor=HITAM, alignment=TA_JUSTIFY,
        ),
        "toc1": ParagraphStyle(
            "Toc1", fontName="Judul-Bold", fontSize=10.5, leading=16,
            textColor=BIRU, spaceBefore=4,
        ),
        "toc2": ParagraphStyle(
            "Toc2", fontName="Isi", fontSize=9.5, leading=13,
            textColor=HITAM, leftIndent=14,
        ),
    }
    return gaya


# ----------------------------------------------------------------------
# Teks kaya
# ----------------------------------------------------------------------
def escape(teks: str) -> str:
    return (teks.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def kaya(teks: str) -> str:
    hasil = []
    for jenis, isi in mdparse.inline_bagian(teks):
        aman = escape(isi)
        if jenis == "tebal":
            hasil.append(f"<b>{aman}</b>")
        elif jenis == "miring":
            hasil.append(f"<i>{aman}</i>")
        elif jenis == "kode":
            hasil.append(
                f'<font name="Kode" size="8.6" color="#9C2A00">{aman}</font>'
            )
        else:
            hasil.append(aman)
    return "".join(hasil)


# ----------------------------------------------------------------------
# Dokumen & templat halaman
# ----------------------------------------------------------------------
class Dokumen(BaseDocTemplate):
    def __init__(self, nama, **kwargs):
        super().__init__(nama, **kwargs)

    def halaman_isi(self, canvas, doc):
        canvas.saveState()
        lebar, tinggi = A4
        # header
        canvas.setFont("Judul", 7.6)
        canvas.setFillColor(ABU)
        canvas.drawRightString(
            lebar - MARGIN_KANAN, tinggi - 1.25 * cm,
            "Tugas Bab 5  ·  Arsitektur Kualitas Perangkat Lunak"
        )
        canvas.setStrokeColor(colors.HexColor("#D6E4F0"))
        canvas.setLineWidth(0.7)
        canvas.line(MARGIN_KIRI, tinggi - 1.45 * cm,
                    lebar - MARGIN_KANAN, tinggi - 1.45 * cm)
        # footer
        canvas.setFont("Judul", 8)
        canvas.setFillColor(ABU)
        canvas.drawCentredString(lebar / 2, 1.15 * cm, str(doc.page))
        canvas.restoreState()

    def halaman_sampul(self, canvas, doc):
        canvas.saveState()
        lebar, tinggi = A4
        # pita atas
        canvas.setFillColor(BIRU)
        canvas.rect(0, tinggi - 10.6 * cm, lebar, 10.6 * cm, stroke=0, fill=1)
        canvas.setFillColor(colors.HexColor("#C55A11"))
        canvas.rect(0, tinggi - 10.85 * cm, lebar, 0.25 * cm, stroke=0, fill=1)

        canvas.setFillColor(colors.white)
        canvas.setFont("Judul-Bold", 10)
        canvas.drawString(MARGIN_KIRI, tinggi - 3.2 * cm, "TUGAS MATA KULIAH")
        canvas.setFont("Judul", 9.5)
        canvas.drawString(MARGIN_KIRI, tinggi - 3.85 * cm,
                          "SOFTWARE QUALITY ASSURANCE (SQA)")

        canvas.setFont("Judul-Bold", 27)
        canvas.drawString(MARGIN_KIRI, tinggi - 6.3 * cm,
                          "Arsitektur Kualitas")
        canvas.drawString(MARGIN_KIRI, tinggi - 7.8 * cm, "Perangkat Lunak")
        canvas.setFont("Judul", 12.5)
        canvas.setFillColor(colors.HexColor("#FBE4D5"))
        canvas.drawString(MARGIN_KIRI, tinggi - 8.8 * cm,
                          "Domain Testing  &  System Integration Testing")

        # blok identitas
        canvas.setFillColor(HITAM)
        y = tinggi - 13.2 * cm
        data = [
            ("Disusun oleh", "Muhammad Arya Fatthurahman"),
            ("NIM", "2023230006"),
            ("Program Studi", "Teknologi Informasi"),
            ("Mata Kuliah", "Software Quality Assurance (SQA)"),
            ("Materi", "Bab 5 — Arsitektur Kualitas Perangkat Lunak"),
        ]
        for k, v in data:
            canvas.setFont("Judul", 9)
            canvas.setFillColor(ABU)
            canvas.drawString(MARGIN_KIRI, y, k)
            canvas.setFont("Isi-Bold", 10.5)
            canvas.setFillColor(HITAM)
            canvas.drawString(MARGIN_KIRI + 4.4 * cm, y, ":  " + v)
            y -= 0.85 * cm

        canvas.setStrokeColor(colors.HexColor("#C55A11"))
        canvas.setLineWidth(1.1)
        canvas.line(MARGIN_KIRI, y - 0.2 * cm, lebar - MARGIN_KANAN, y - 0.2 * cm)

        canvas.setFont("Isi-Italic", 9.4)
        canvas.setFillColor(ABU)
        canvas.drawString(
            MARGIN_KIRI, y - 1.1 * cm,
            "Jawaban 10 soal esai, analisis batas domain, taksonomi cacat,"
        )
        canvas.drawString(
            MARGIN_KIRI, y - 1.65 * cm,
            "dan strategi pengujian integrasi sistem."
        )

        canvas.setFont("Judul-Bold", 10)
        canvas.setFillColor(BIRU)
        canvas.drawString(MARGIN_KIRI, 2.4 * cm, "2026")
        canvas.setFont("Judul", 8)
        canvas.setFillColor(ABU)
        canvas.drawRightString(lebar - MARGIN_KANAN, 2.4 * cm,
                              "Dokumen ini dihasilkan dari sumber Markdown "
                              "yang sama dengan versi Word")
        canvas.restoreState()


def buat_dokumen(tujuan: str) -> Dokumen:
    doc = Dokumen(
        tujuan, pagesize=A4,
        leftMargin=MARGIN_KIRI, rightMargin=MARGIN_KANAN,
        topMargin=MARGIN_ATAS, bottomMargin=MARGIN_BAWAH,
        title="Tugas Bab 5 - Arsitektur Kualitas Perangkat Lunak",
        author="Muhammad Arya Fatthurahman",
        subject="Software Quality Assurance",
    )
    bingkai = Frame(MARGIN_KIRI, MARGIN_BAWAH, LEBAR_ISI,
                    TINGGI_HALAMAN - MARGIN_ATAS - MARGIN_BAWAH,
                    id="isi", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="sampul", frames=[bingkai], onPage=doc.halaman_sampul),
        PageTemplate(id="isi", frames=[bingkai], onPage=doc.halaman_isi),
    ])
    return doc


# ----------------------------------------------------------------------
# Flowable per blok
# ----------------------------------------------------------------------
def flowable_table(headers: Sequence[str], rows: Sequence[Sequence[str]],
                   gaya: dict) -> Table:
    lebar = _bagi_lebar(headers, rows)
    data = [[Paragraph(mdparse.teks_bersih(str(h)), gaya["sel_head"])
             for h in headers]]
    for r in rows:
        baris = [Paragraph(kaya(str(x)), gaya["sel"]) for x in r]
        while len(baris) < len(headers):
            baris.append(Paragraph("", gaya["sel"]))
        data.append(baris)
    t = Table(data, colWidths=lebar, repeatRows=1, hAlign="CENTER")
    perintah = [
        ("BACKGROUND", (0, 0), (-1, 0), BIRU),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFD0E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            perintah.append(("BACKGROUND", (0, i), (-1, i),
                             colors.HexColor("#F2F6FA")))
    t.setStyle(TableStyle(perintah))
    return t


def _lebar_baris(teks: str) -> tuple[float, float]:
    """Lebar (kata terpanjang, seluruh teks) sesuai gaya inline sebenarnya."""
    kata = penuh = 0.0
    for jenis, isi in mdparse.inline_bagian(teks):
        if jenis == "kode":
            font, ukuran = "Kode", 8.6
        elif jenis == "tebal":
            font, ukuran = "Isi-Bold", 7.9
        else:
            font, ukuran = "Isi", 7.9
        penuh += stringWidth(isi, font, ukuran)
        kata = max(kata, max((stringWidth(w, font, ukuran)
                              for w in isi.split()), default=0.0))
    return kata, penuh


def _bagi_lebar(headers, rows) -> List[float]:
    """Bagi lebar kolom berdasarkan lebar teks sebenarnya, bukan jumlah huruf.

    Setiap kolom mendapat lebar minimum yang cukup untuk kata terpanjang
    (agar nama berkas seperti ``soal04_kompleksitas.cpp`` tidak terpotong),
    lalu sisa lebar dibagikan sesuai panjang isi sel.
    """
    jumlah = len(headers)
    # 8 pt untuk padding sel + sisa aman agar kata tidak patah di ujung
    pad = 12.0
    minimum: List[float] = []
    alami: List[float] = []
    for i in range(jumlah):
        teks_kolom = [str(headers[i])]
        teks_kolom += [str(r[i]) for r in rows if i < len(r)]
        hasil = [_lebar_baris(t) for t in teks_kolom]
        kata = max((k for k, _ in hasil), default=0.0)
        kata = max(kata, stringWidth(mdparse.teks_bersih(str(headers[i])),
                                     "Judul-Bold", 8.1))
        penuh = max((p for _, p in hasil), default=0.0)
        minimum.append(kata + pad)
        alami.append(min(penuh + pad, LEBAR_ISI * 0.62))

    total_min = sum(minimum)
    if total_min >= LEBAR_ISI:
        skala = LEBAR_ISI / total_min
        return [w * skala for w in minimum]

    sisa = LEBAR_ISI - total_min
    bobot = [max(0.0, a - m) for a, m in zip(alami, minimum)]
    total_bobot = sum(bobot)
    if total_bobot <= 0:
        return [m + sisa / jumlah for m in minimum]
    return [m + sisa * b / total_bobot for m, b in zip(minimum, bobot)]


def flowable_kode(teks: str, gaya: dict) -> "KotakKode":
    return KotakKode(teks.replace("\t", "    "), gaya["kode"], LEBAR_ISI)


class KotakKode(Flowable):
    """Blok kode dengan latar abu-abu, bingkai, dan dukungan pemisahan halaman."""

    def __init__(self, teks: str, gaya: ParagraphStyle, lebar: float):
        super().__init__()
        self.baris = teks.split("\n")
        self.gaya = gaya
        self.lebar = lebar
        self.pad = 6
        self.ukuran = gaya.fontSize
        self.leading = gaya.leading
        # sesuaikan ukuran huruf bila ada baris yang terlalu panjang
        maks = max((stringWidth(b, gaya.fontName, self.ukuran) for b in self.baris),
                   default=0)
        if maks > lebar - 2 * self.pad and maks > 0:
            self.ukuran = max(5.6, self.ukuran * (lebar - 2 * self.pad) / maks)
            self.leading = self.ukuran * 1.28
        self.height = len(self.baris) * self.leading + 2 * self.pad

    def wrap(self, lebar_tersedia, tinggi_tersedia):
        self.lebar = min(self.lebar, lebar_tersedia)
        self.height = len(self.baris) * self.leading + 2 * self.pad
        return self.lebar, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(LATAR_KODE)
        c.setStrokeColor(colors.HexColor("#E2E2DE"))
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self.lebar, self.height, 2, stroke=1, fill=1)
        c.setFont(self.gaya.fontName, self.ukuran)
        c.setFillColor(colors.HexColor("#222222"))
        y = self.height - self.pad - self.ukuran
        for b in self.baris:
            c.drawString(self.pad, y, b)
            y -= self.leading
        c.restoreState()

    def split(self, lebar_tersedia, tinggi_tersedia):
        if self.height <= tinggi_tersedia:
            return [self]
        muat = int((tinggi_tersedia - 2 * self.pad) // self.leading)
        if muat < 4:
            return []
        kepala = KotakKode("\n".join(self.baris[:muat]),
                           self.gaya, self.lebar)
        ekor = KotakKode("\n".join(self.baris[muat:]),
                         self.gaya, self.lebar)
        return [kepala, ekor]


def flowable_gambar(path: str, lebar_cm: float | None, gaya: dict,
                    keterangan: str) -> List:
    from PIL import Image as PILImage

    with PILImage.open(path) as im:
        w, h = im.size
    lebar = min((lebar_cm or 14.5) * cm, 15.4 * cm)
    tinggi = lebar * h / w
    maks = 20.5 * cm
    if tinggi > maks:
        tinggi = maks
        lebar = tinggi * w / h
    hasil = [Spacer(1, 4), Image(path, width=lebar, height=tinggi)]
    if keterangan:
        hasil.append(Paragraph(escape(keterangan), gaya["caption"]))
    return hasil


def flowable_catatan(teks: str, gaya: dict) -> Table:
    t = Table([[Paragraph(kaya(teks), gaya["note"])]],
              colWidths=[LEBAR_ISI], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF1F8")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#B6CBE4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def daftar_isi(blok: Sequence[Blok], gaya: dict) -> List:
    gaya_cap = ParagraphStyle("TocCap", parent=gaya["caption"],
                              alignment=TA_LEFT)
    hasil = [Paragraph("Daftar Isi", gaya["h1"]),
             Paragraph("Struktur dokumen jawaban ini:", gaya_cap)]
    for b in blok:
        if b.jenis != "h" or b.level > 2:
            continue
        teks = mdparse.teks_bersih(b.isi)
        gaya_toc = gaya["toc1"] if b.level == 1 else gaya["toc2"]
        hasil.append(Paragraph(escape(teks), gaya_toc))
    hasil.append(PageBreak())
    return hasil


def bangun(berkas_md: str, tujuan: str) -> None:
    daftarkan_font()
    gaya = buat_gaya()
    blok = mdparse.parse(berkas_md)
    doc = buat_dokumen(tujuan)

    cerita: List = [NextPageTemplate("isi"), PageBreak()]
    cerita += daftar_isi(blok, gaya)

    pertama = True
    for b in blok:
        if b.jenis == "h":
            if b.level == 1:
                if not pertama:
                    cerita.append(PageBreak())
                pertama = False
                cerita.append(Paragraph(escape(mdparse.teks_bersih(b.isi)),
                                        gaya["h1"]))
            else:
                cerita.append(Paragraph(escape(mdparse.teks_bersih(b.isi)),
                                        gaya[f"h{b.level}"]))
        elif b.jenis == "p":
            cerita.append(Paragraph(kaya(b.isi), gaya["isi"]))
        elif b.jenis in ("ul", "ol"):
            items = [ListItem(Paragraph(kaya(x), gaya["daftar"]),
                              leftIndent=22) for x in b.isi]
            cerita.append(ListFlowable(
                items, bulletType="1" if b.jenis == "ol" else "bullet",
                bulletFormat="%s." if b.jenis == "ol" else None,
                bulletFontName="Judul-Bold" if b.jenis == "ol" else "Judul",
                bulletFontSize=8.4,
                leftIndent=27 if b.jenis == "ol" else 18,
                bulletDedent=20 if b.jenis == "ol" else 16, spaceAfter=6,
            ))
        elif b.jenis == "code":
            cerita.append(flowable_kode(b.isi, gaya))
            cerita.append(Spacer(1, 6))
        elif b.jenis == "table":
            headers, rows = b.isi
            cerita.append(flowable_table(headers, rows, gaya))
            cerita.append(Spacer(1, 7))
        elif b.jenis == "img":
            cerita += flowable_gambar(b.isi, b.level, gaya, b.bahasa)
        elif b.jenis == "note":
            cerita.append(flowable_catatan(b.isi, gaya))
            cerita.append(Spacer(1, 7))
        elif b.jenis == "caption":
            cerita.append(Paragraph(escape(b.isi), gaya["caption"]))
        elif b.jenis == "break":
            cerita.append(PageBreak())

    doc.build(cerita)
    print(f"[OK] PDF   : {tujuan}")


if __name__ == "__main__":
    akar = os.path.dirname(os.path.abspath(__file__))
    bangun(os.path.join(akar, "isi_tugas.md"),
           os.path.join(akar, "Tugas_Bab5_Arsitektur_Kualitas.pdf"))
