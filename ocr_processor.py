import pytesseract
from PIL import Image
import os

folder_gambar = "novel_mie_ayam"
file_output = "teks_mie_ayam.txt"

# Mengurutkan file agar halaman 001 sampai 430 terbaca sesuai urutan
files = sorted([f for f in os.listdir(folder_gambar) if f.endswith('.webp')])

print("[-] Memulai proses OCR (membaca gambar ke teks)...")

with open(file_output, "w", encoding="utf-8") as f:
    for file in files:
        print(f"--> Memproses {file}...")
        teks = pytesseract.image_to_string(Image.open(os.path.join(folder_gambar, file)), lang='ind')
        f.write(f"\n--- {file} ---\n\n")
        f.write(teks)

print(f"\n[V] Selesai! Seluruh teks novel telah tersimpan di {file_output}")
