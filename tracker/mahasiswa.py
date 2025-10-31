# tracker/mahasiswa.py

class Mahasiswa:
    """
    Merepresentasikan seorang mahasiswa dengan data nim, nama,
    dan persentase kehadiran yang divalidasi [cite: 819-822].
    """
    
    def __init__(self, nim, nama):
        """
        Inisialisasi objek Mahasiswa.
        
        Args:
            nim (str): Nomor Induk Mahasiswa.
            nama (str): Nama lengkap mahasiswa.
        """
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0.0  # Atribut internal [cite: 820]

    @property
    def hadir_persen(self):
        """
        Properti untuk mendapatkan nilai _hadir_persen.
        """
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, v):
        """
        Setter untuk memvalidasi dan mengatur _hadir_persen.
        Nilai harus antara 0 dan 100[cite: 821, 875].
        """
        try:
            v_float = float(v)
        except ValueError:
            raise ValueError("Persentase kehadiran harus berupa angka.")
            
        if not (0 <= v_float <= 100):
            raise ValueError("Persentase kehadiran harus antara 0..100")
        self._hadir_persen = v_float

    def info(self):
        """
        Menampilkan profil singkat mahasiswa (sesuai ketentuan tugas).
        """
        return f"Profil Mhs: {self.nim} - {self.nama}, Hadir: {self.hadir_persen:.2f}%"

    def __repr__(self):
        """
        Representasi string objek untuk debugging.
        """
        return f"<Mahasiswa {self.nim} {self.nama} hadir={self.hadir_persen:.2f}%>"