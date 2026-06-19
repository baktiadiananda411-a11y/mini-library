import os
import re

file_ocr = "teks_mie_ayam.txt"
folder_output = "bab_html"

if not os.path.exists(folder_output):
    os.makedirs(folder_output)

with open(file_ocr, 'r', encoding='utf-8') as f:
    konten = f.read()

# Memecah berdasarkan penanda halaman
parts = re.split(r'---\s+halaman_(\d{3})\.webp\s+---', konten)

pages = []
for i in range(1, len(parts), 2):
    nomor_hal = parts[i]
    isi_hal = parts[i+1].strip()
    pages.append({"nomor": nomor_hal, "isi": isi_hal})

total_pages = len(pages)

# Daftar halaman gambar
halaman_gambar = ["001", "002", "004", "005", "007", "025", "037", "051", "071", "091", "118", "119", "137", "159", "177", "203", "204", "217"]

for i, page in enumerate(pages):
    nomor = page['nomor']
    isi_mentah = page['isi']
    
    isi_rapi = '<p>' + isi_mentah.replace('\n\n', '</p><p>') + '</p>'
    isi_rapi = isi_rapi.replace('\n', ' ')
    
    # Nama file baru dengan prefix 'ma_' agar tidak tertukar dengan novel lain
    nama_file = f"ma_halaman_{nomor}.html"
    
    # Navigasi dengan prefix baru
    prev_file = f"ma_halaman_{pages[i-1]['nomor']}.html" if i > 0 else "../index_mie_ayam.html"
    next_file = f"ma_halaman_{pages[i+1]['nomor']}.html" if i < total_pages - 1 else "../index_mie_ayam.html"
    
    # Logic gambar
    if nomor in halaman_gambar:
        tag_gambar = f'<img src="../novel_mie_ayam/halaman_{nomor}.webp" alt="Ilustrasi {nomor}" class="page-img">'
        isi_rapi = ""
    else:
        tag_gambar = ""

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halaman {nomor} - Mie Ayam</title>
    <style>
        body {{ background-color: #0f0f0f; color: #e0e0e0; font-family: sans-serif; line-height: 1.8; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 40px auto; background-color: #1e1e1e; padding: 40px; border-radius: 12px; border: 1px solid #333; }}
        .page-img {{ display: block; max-width: 100%; margin: 0 auto 30px; border-radius: 8px; }}
        .nav-btn {{ background-color: #2c2c2c; color: #bb86fc; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; border: 1px solid #bb86fc; }}
        .back-index {{ display: block; text-align: center; margin-top: 40px; color: #888; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Halaman {nomor}</h1>
        {tag_gambar}
        <div>{isi_rapi}</div>
        <div style="display: flex; justify-content: space-between; margin-top: 30px;">
            <a href="{prev_file}" class="nav-btn">⬅️ Sebelumnya</a>
            <a href="{next_file}" class="nav-btn">Selanjutnya ➡️</a>
        </div>
        <a href="../index_mie_ayam.html" class="back-index">Kembali ke Daftar Isi</a>
    </div>
</body>
</html>
"""
    with open(os.path.join(folder_output, nama_file), 'w', encoding='utf-8') as f:
        f.write(html_content)

print("Selesai! File baru dengan prefix 'ma_' sudah dibuat.")
