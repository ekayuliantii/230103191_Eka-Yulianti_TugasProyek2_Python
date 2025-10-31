# tracker/rekap_kelas.py

# Impor kelas lain dari dalam paket 'tracker'
from .penilaian import Penilaian

class RekapKelas:
    """
    Manajer utama yang mengelola (mengagregasi) semua objek Mahasiswa
    dan Penilaian yang terkait.
    
    Data disimpan dalam dictionary dengan NIM sebagai kunci.
    [cite: 641, 642, 643, 644]
    """
    
    def __init__(self):
        """
        Inisialisasi RekapKelas.
        Membuat dictionary internal _by_nim untuk menyimpan data.
        """
        # Struktur: {nim: {'mhs': ObjekMahasiswa, 'nilai': ObjekPenilaian}}
        self._by_nim = {}

    def tambah_mahasiswa(self, mhs):
        """
        Menambahkan objek Mahasiswa baru ke dalam rekap.
        Secara otomatis membuat objek Penilaian kosong untuk mahasiswa tsb.
        [cite: 646]
        
        Args:
            mhs (Mahasiswa): Objek Mahasiswa yang akan ditambahkan.
        """
        if mhs.nim in self._by_nim:
            raise ValueError(f"NIM {mhs.nim} sudah ada.")
        
        self._by_nim[mhs.nim] = {'mhs': mhs, 'nilai': Penilaian()}

    def _get_item_by_nim(self, nim):
        """Helper internal untuk mengambil data mhs/nilai berdasarkan NIM."""
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError(f"NIM {nim} tidak ditemukan dalam rekap.")
        return item

    def set_hadir(self, nim, persen):
        """
        Mengatur persentase kehadiran untuk mahasiswa berdasarkan NIM.
        [cite: 647]
        
        Args:
            nim (str): NIM mahasiswa yang akan diupdate.
            persen (float/int): Nilai persentase kehadiran (0-100).
        """
        item = self._get_item_by_nim(nim)
        item['mhs'].hadir_persen = persen # Gunakan property setter

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        """
        Mengatur nilai (quiz, tugas, uts, uas) untuk mahasiswa berdasarkan NIM.
        Nilai yang None akan diabaikan.
        [cite: 648]
        
        Args:
            nim (str): NIM mahasiswa yang akan diupdate.
            quiz (float, optional): Nilai quiz baru.
            tugas (float, optional): Nilai tugas baru.
            uts (float, optional): Nilai UTS baru.
            uas (float, optional): Nilai UAS baru.
        """
        item = self._get_item_by_nim(nim)
        p = item['nilai']
        
        if quiz is not None:
            p.quiz = quiz
        if tugas is not None:
            p.tugas = tugas
        if uts is not None:
            p.uts = uts
        if uas is not None:
            p.uas = uas

    def predikat(self, skor):
        """
        Menentukan predikat huruf (A-E) berdasarkan skor akhir.
        [cite: 650]
        
        Args:
            skor (float): Nilai akhir (0-100).
            
        Returns:
            str: Predikat huruf (A, B, C, D, atau E).
        """
        if skor >= 85:
            return "A"
        if skor >= 75:
            return "B"
        if skor >= 65:
            return "C"
        if skor >= 50:
            return "D"
        return "E"

    def rekap(self):
        """
        Menghasilkan rekapitulasi lengkap semua mahasiswa.
        [cite: 649]
        
        Returns:
            list: Daftar dictionary (list of dict) berisi rekap data
                  per mahasiswa (nim, nama, hadir, akhir, predikat).
        """
        rows = []
        for nim, data in self._by_nim.items():
            mhs = data['mhs']
            penilaian = data['nilai']
            
            skor_akhir = penilaian.nilai_akhir()
            
            rows.append({
                'nim': mhs.nim,
                'nama': mhs.nama,
                'hadir': mhs.hadir_persen,
                'akhir': skor_akhir,
                'predikat': self.predikat(skor_akhir),
            })
        return rows