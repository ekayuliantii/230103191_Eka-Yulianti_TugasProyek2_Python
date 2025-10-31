# tracker/penilaian.py

class Penilaian:
    """
    Merepresentasikan komponen nilai seorang mahasiswa (quiz, tugas, uts, uas)
    dan menghitung nilai akhirnya.
    
    Semua nilai divalidasi harus antara 0-100[cite: 346].
    """
    
    def __init__(self, quiz=0, tugas=0, uts=0, uas=0):
        """
        Inisialisasi objek Penilaian.
        
        Args:
            quiz (float, optional): Nilai quiz. Default ke 0.
            tugas (float, optional): Nilai tugas. Default ke 0.
            uts (float, optional): Nilai UTS. Default ke 0.
            uas (float, optional): Nilai UAS. Default ke 0.
        """
        # Atribut internal (protected)
        self._quiz = 0.0
        self._tugas = 0.0
        self._uts = 0.0
        self._uas = 0.0
        
        # Gunakan setter saat inisialisasi untuk validasi
        self.quiz = quiz
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

    def _validate(self, v):
        """Metode helper internal untuk validasi nilai 0-100."""
        try:
            v_float = float(v)
        except ValueError:
            raise ValueError("Nilai harus berupa angka.")
            
        if not (0 <= v_float <= 100):
            raise ValueError("Nilai harus antara 0..100")
        return v_float

    # --- Properti untuk Quiz ---
    @property
    def quiz(self):
        """Properti untuk mendapatkan nilai _quiz."""
        return self._quiz
    
    @quiz.setter
    def quiz(self, v):
        """Setter untuk memvalidasi dan mengatur _quiz."""
        self._quiz = self._validate(v) 
    # --- Properti untuk Tugas ---
    @property
    def tugas(self):
        """Properti untuk mendapatkan nilai _tugas."""
        return self._tugas
    
    @tugas.setter
    def tugas(self, v):
        """Setter untuk memvalidasi dan mengatur _tugas."""
        self._tugas = self._validate(v) 
    # --- Properti untuk UTS ---
    @property
    def uts(self):
        """Properti untuk mendapatkan nilai _uts."""
        return self._uts
    
    @uts.setter
    def uts(self, v):
        """Setter untuk memvalidasi dan mengatur _uts."""
        self._uts = self._validate(v)

    # --- Properti untuk UAS ---
    @property
    def uas(self):
        """Properti untuk mendapatkan nilai _uas."""
        return self._uas
    
    @uas.setter
    def uas(self, v):
        """Setter untuk memvalidasi dan mengatur _uas."""
        self._uas = self._validate(v) 

    def nilai_akhir(self):
        """
        Menghitung nilai akhir berdasarkan bobot yang ditentukan.
        Bobot: Quiz 15%, Tugas 25%, UTS 25%, UAS 35%[cite: 345].
        
        Returns:
            float: Nilai akhir yang sudah dibulatkan.
        """
        skor = (
            self.quiz * 0.15 +
            self.tugas * 0.25 +
            self.uts * 0.25 +
            self.uas * 0.35
        )
        return round(skor, 2)

    def __repr__(self):
        """Representasi string objek untuk debugging."""
        return f"<Penilaian q={self.quiz} t={self.tugas} uts={self.uts} uas={self.uas}>"