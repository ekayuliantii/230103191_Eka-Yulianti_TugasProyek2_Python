# tracker/_main_.py
# File ini memungkinkan program dijalankan langsung dengan:
#     python -m tracker

from app import menu

def main():
    """Menjalankan menu utama aplikasi Student Performance Tracker."""
    print("🔹 Mode Paket Tracker aktif (dijalankan via python -m tracker) 🔹\n")
    menu()

if __name__ == "__main__":
    main()