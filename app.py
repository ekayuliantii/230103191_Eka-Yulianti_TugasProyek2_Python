"""
app.py
======

File utama untuk menjalankan aplikasi Student Performance Tracker.
Berisi logika utama seperti pemuatan data, tampilan rekap, 
dan menu interaktif CLI.
"""

import csv
from pathlib import Path

# Impor kelas dan fungsi dari paket 'tracker'
from tracker import (
    Mahasiswa,
    RekapKelas,
    build_markdown_report,
    save_text
)

# --- Gunakan 'rich' untuk tampilan berwarna & tabel interaktif ---
try:
    from rich import print
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
except ImportError:
    print("Modul 'rich' tidak ditemukan. Gunakan: pip install rich")
    Table = None
    console = None


# =========================================================
#  FUNGSI PEMUAT DATA
# =========================================================
def load_csv(path):
    """
    Membaca file CSV dan mengembalikannya sebagai list of dict.

    Args:
        path (str): Lokasi file CSV yang akan dibaca.

    Returns:
        list[dict]: Isi file CSV dalam bentuk list of dict,
                    atau list kosong jika file tidak ditemukan.
    """
    try:
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"[red]⚠ File tidak ditemukan: {path}[/red]")
        return []


def bootstrap_from_csv(rekap, att_path="data/attendance.csv", grd_path="data/grades.csv"):
    """
    Memuat data kehadiran dan nilai dari file CSV lalu mengisi objek RekapKelas.

    Args:
        rekap (RekapKelas): Objek rekap kelas yang akan diisi.
        att_path (str): Lokasi file attendance.csv.
        grd_path (str): Lokasi file grades.csv.
    """
    att = load_csv(att_path)
    grd = load_csv(grd_path)

    if not att or not grd:
        print("[yellow]⚠ Data tidak dimuat. Pastikan file attendance.csv dan grades.csv tersedia.[/yellow]")
        return

    for row in att:
        if "student_id" not in row or "name" not in row:
            print(f"[yellow]Baris data tidak valid: {row}[/yellow]")
            continue

        m = Mahasiswa(row["student_id"], row["name"])
        try:
            rekap.tambah_mahasiswa(m)
        except ValueError as e:
            print(f"[cyan]ℹ {e}[/cyan]")

        minggu = [k for k in row.keys() if k.startswith("week")]
        if minggu:
            total = len(minggu)
            hadir = sum(int(row[w].strip()) for w in minggu if row[w].strip() != "")
            persen = round(hadir / total * 100, 2)
            rekap.set_hadir(m.nim, persen)

    by_nim = {g["student_id"]: g for g in grd if "student_id" in g}
    for nim in list(rekap._by_nim.keys()):
        g = by_nim.get(nim)
        if g:
            rekap.set_penilaian(
                nim,
                quiz=float(g.get("quiz", 0) or 0),
                tugas=float(g.get("assignment", 0) or 0),
                uts=float(g.get("mid", 0) or 0),
                uas=float(g.get("final", 0) or 0),
            )
    print("[green]✅ Data berhasil dimuat dari CSV.[/green]")


# =========================================================
#  FUNGSI TAMPILAN REKAP
# =========================================================
def tampilkan_rekap(rows):
    """
    Menampilkan hasil rekap mahasiswa ke terminal (dalam tabel Rich atau teks biasa).

    Args:
        rows (list[dict]): Daftar hasil rekap mahasiswa.
    """
    if not rows:
        print("[yellow]⚠ Belum ada data untuk ditampilkan.[/yellow]")
        return

    if Table:
        table = Table(title="📊 Rekap Kinerja Mahasiswa", title_style="bold cyan")
        table.add_column("NIM", justify="center", style="bold white")
        table.add_column("Nama", style="bold green")
        table.add_column("Hadir (%)", justify="right", style="yellow")
        table.add_column("Nilai Akhir", justify="right", style="magenta")
        table.add_column("Predikat", justify="center", style="bold blue")

        for r in rows:
            table.add_row(
                r['nim'],
                r['nama'],
                f"{r['hadir']:.2f}",
                f"{r['akhir']:.2f}",
                r['predikat']
            )
        console.print(table)
    else:
        print("\n--- REKAP KINERJA MAHASISWA ---")
        for r in rows:
            print(f"{r['nim']} | {r['nama']} | Hadir: {r['hadir']}% | Nilai: {r['akhir']} | Predikat: {r['predikat']}")


# =========================================================
#  FUNGSI SIMPAN LAPORAN
# =========================================================
def simpan_laporan(rekap_objek):
    """
    Menyimpan laporan hasil rekap ke file Markdown (.md).

    Args:
        rekap_objek (RekapKelas): Objek berisi data mahasiswa.
    """
    records = rekap_objek.rekap()
    if not records:
        print("[red]❌ Tidak ada data untuk disimpan.[/red]")
        return

    md_content = build_markdown_report(records)
    output_path = Path("out") / "report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        save_text(str(output_path), md_content)
        print(f"[green]💾 Laporan berhasil disimpan di [bold]{output_path}[/bold][/green]")
    except Exception as e:
        print(f"[red]Gagal menyimpan laporan: {e}[/red]")


def simpan_laporan_html(rekap_objek):
    """
    Menyimpan laporan hasil rekap ke file HTML (.html).

    Args:
        rekap_objek (RekapKelas): Objek berisi data mahasiswa.
    """
    from tracker.report import build_html_report, save_text

    records = rekap_objek.rekap()
    if not records:
        print("[red]❌ Tidak ada data untuk dilaporkan.[/red]")
        return

    html_content = build_html_report(records)
    output_path = Path("out") / "report.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        save_text(str(output_path), html_content)
        print(f"[green]🌐 Laporan HTML berhasil disimpan di [bold]{output_path}[/bold][/green]")
    except Exception as e:
        print(f"[red]Gagal menyimpan laporan HTML: {e}[/red]")


# =========================================================
#  MENU UTAMA
# =========================================================
def menu():
    """
    Menampilkan menu utama aplikasi CLI dan menjalankan fitur sesuai pilihan pengguna.
    """
    rekap = RekapKelas()

    while True:
        if console:
            console.print(Panel.fit("🎓 [bold cyan]STUDENT PERFORMANCE TRACKER[/bold cyan]", border_style="blue"))
        else:
            print("\n=== STUDENT PERFORMANCE TRACKER ===")

        print("1) Muat data dari CSV")
        print("2) Tambah mahasiswa")
        print("3) Ubah presensi")
        print("4) Ubah nilai")
        print("5) Lihat rekap")
        print("6) Simpan laporan Markdown")
        print("7) Tampilkan mahasiswa dengan nilai <70")
        print("8) Simpan laporan HTML")
        print("9) Keluar")

        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                bootstrap_from_csv(rekap)
            elif pilihan == "2":
                nim = input("Masukkan NIM: ").strip()
                nama = input("Masukkan Nama: ").strip()
                if not nim or not nama:
                    print("[yellow]⚠ NIM dan Nama tidak boleh kosong.[/yellow]")
                    continue
                rekap.tambah_mahasiswa(Mahasiswa(nim, nama))
                print(f"[green]✅ Mahasiswa {nama} berhasil ditambahkan.[/green]")
            elif pilihan == "3":
                nim = input("Masukkan NIM: ").strip()
                hadir = float(input("Persentase Kehadiran (%): ").strip())
                rekap.set_hadir(nim, hadir)
                print("[green]✅ Data presensi diperbarui.[/green]")
            elif pilihan == "4":
                nim = input("Masukkan NIM: ").strip()
                q = float(input("Nilai Quiz: ").strip())
                t = float(input("Nilai Tugas: ").strip())
                u = float(input("Nilai UTS: ").strip())
                a = float(input("Nilai UAS: ").strip())
                rekap.set_penilaian(nim, quiz=q, tugas=t, uts=u, uas=a)
                print("[green]✅ Nilai berhasil disimpan.[/green]")
            elif pilihan == "5":
                tampilkan_rekap(rekap.rekap())
            elif pilihan == "6":
                simpan_laporan(rekap)
            elif pilihan == "7":
                records = rekap.rekap()
                remedial = [r for r in records if r["akhir"] < 70]
                if remedial:
                    print("[cyan]📉 Mahasiswa dengan nilai di bawah 70:[/cyan]")
                    tampilkan_rekap(remedial)
                else:
                    print("[green]✅ Tidak ada mahasiswa remedial![/green]")
            elif pilihan == "8":
                simpan_laporan_html(rekap)
            elif pilihan == "9":
                print("[cyan]👋 Terima kasih telah menggunakan aplikasi ini![/cyan]")
                break
            else:
                print("[yellow]⚠ Pilihan tidak dikenal, coba lagi.[/yellow]")
        except Exception as e:
            print(f"[red]❌ Terjadi kesalahan: {e}[/red]")


# =========================================================
#  TITIK MASUK UTAMA
# =========================================================
if __name__ == "__main__":
    """Menjalankan fungsi menu() saat file ini dieksekusi langsung."""
    menu()
