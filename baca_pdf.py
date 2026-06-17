import os

pdf_file = "hujan.pdf"
output_teks = "teks_hujan.txt"

if not os.path.exists(pdf_file):
    print(f"[X] File {pdf_file} tidak ditemukan! Pastikan namanya benar.")
    exit()

# 1. Buat folder sementara untuk menyimpan potongan gambar halaman
os.system("mkdir -p temp_gambar")

# 2. Pecah PDF menjadi gambar JPEG (Ini sangat cepat!)
print("1/3 - Memecah PDF menjadi gambar...")
os.system(f"pdftoppm -jpeg {pdf_file} temp_gambar/hal")

# 3. Baca teks dari setiap gambar menggunakan Tesseract OCR
gambar_list = sorted([g for g in os.listdir("temp_gambar") if g.endswith(".jpg")])
jumlah_hal = len(gambar_list)

print(f"2/3 - Memulai proses OCR (Membaca teks dari {jumlah_hal} halaman)...")
print("Proses ini memakan waktu beberapa menit. Silakan ngopi dulu! ☕")

with open(output_teks, "w", encoding="utf-8") as f:
    for i, img in enumerate(gambar_list):
        print(f"  -> Membaca halaman {i+1} dari {jumlah_hal}...", end="\r")
        
        # Ekstrak teks (menggunakan bahasa Indonesia)
        os.system(f"tesseract temp_gambar/{img} temp_teks -l ind > /dev/null 2>&1")
        
        # Baca hasil ekstrak
        with open("temp_teks.txt", "r", encoding="utf-8") as tf:
            teks = tf.read()
        
        # Format angka agar sesuai (misal: hal-001.jpg jadi 001)
        hal_num = img.replace("hal-", "").replace(".jpg", "")
        
        # Tulis ke file mentahan dengan format penanda
        f.write(f"\n--- halaman_{hal_num}.webp ---\n")
        f.write(teks)
        f.write("\n")

print(f"\n\n3/3 - [V] SELESAI! Teks mentah berhasil disimpan di {output_teks}")

# Bersihkan file sampah sementara
os.system("rm -rf temp_gambar temp_teks.txt")
