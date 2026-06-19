import os
import re

file_ocr = "teks_hujan.txt"
folder_output = "bab_html"
folder_gambar = "novel_hujan"

if not os.path.exists(folder_output):
    os.makedirs(folder_output)

with open(file_ocr, 'r', encoding='utf-8') as f:
    konten = f.read()

# Memecah berdasarkan pola penanda halaman
parts = re.split(r'---\s+halaman_(\d{3})\.(?:webp|jpg|png)\s+---', konten)

pages = []
for i in range(1, len(parts), 2):
    nomor_hal = parts[i]
    isi_hal = parts[i+1].strip()
    pages.append({"nomor": nomor_hal, "isi": isi_hal})

total_pages = len(pages)

for i, page in enumerate(pages):
    nomor = page['nomor']
    isi_mentah = page['isi']
    
    isi_rapi = '<p>' + isi_mentah.replace('\n\n', '</p><p>') + '</p>'
    isi_rapi = isi_rapi.replace('\n', ' ')
    
    # Nama file HTML dengan prefix 'hj_' agar tidak tabrakan dengan Mie Ayam
    nama_file = f"hj_halaman_{nomor}.html"
    
    # Link navigasi antar halaman
    prev_link = f"hj_halaman_{pages[i-1]['nomor']}.html" if i > 0 else "../index.html"
    next_link = f"hj_halaman_{pages[i+1]['nomor']}.html" if i < total_pages - 1 else "../index.html"

    # --- LOGIKA GAMBAR (DIUBAH KE .jpg SESUAI SCREENSHOT KAMU) ---
    path_gambar = os.path.join(folder_gambar, f"halaman_{nomor}.jpg")
    
    if os.path.exists(path_gambar):
        tag_gambar = f'<img src="../{folder_gambar}/halaman_{nomor}.jpg" alt="Ilustrasi Halaman {nomor}" class="page-img">'
        isi_rapi = "" # Teks OCR disembunyikan jika halaman ini adalah gambar/cover
    else:
        tag_gambar = ""

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halaman {nomor} - Hujan</title>
    <style>
        body {{ background-color: #0f0f0f; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; line-height: 1.8; margin: 0; padding: 20px; transition: 0.3s; }}
        .container {{ max-width: 800px; margin: 40px auto; background-color: #1e1e1e; padding: 40px; border-radius: 12px; border: 1px solid #333; }}
        h1 {{ color: #555; text-align: center; margin-bottom: 20px; font-size: 1.2em; border-bottom: 1px dashed #333; padding-bottom: 15px; text-transform: uppercase; }}
        p {{ margin-bottom: 20px; font-size: 1.1em; text-align: justify; color: #ccc; }}
        .page-img {{ display: block; max-width: 100%; height: auto; margin: 0 auto 30px auto; border-radius: 8px; border: 1px solid #444; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }}
        .nav-buttons {{ display: flex; justify-content: space-between; margin: 30px 0; }}
        .nav-btn {{ background-color: #2c2c2c; color: #bb86fc; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; border: 1px solid #bb86fc; }}
        .nav-btn:hover {{ background-color: #bb86fc; color: #121212; }}
        .back-index {{ display: block; text-align: center; margin-top: 40px; color: #888; text-decoration: none; font-size: 0.9em; }}
        .back-index:hover {{ color: #bb86fc; }}
        
        /* TEMA TERANG */
        body.light-mode {{ background-color: #f4f4f4; color: #333; }}
        body.light-mode .container {{ background-color: #ffffff; border-color: #ddd; }}
        body.light-mode h1 {{ color: #5e35b1; border-bottom-color: #ddd; }}
        body.light-mode p {{ color: #222; }}
        body.light-mode .nav-btn {{ background-color: #ffffff; color: #5e35b1; border-color: #5e35b1; }}
        body.light-mode .nav-btn:hover {{ background-color: #5e35b1; color: #ffffff; }}
        body.light-mode .back-index {{ color: #5e35b1; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Halaman {nomor}</h1>
        {tag_gambar}
        <div>{isi_rapi}</div>
        <div class="nav-buttons">
            <a href="{prev_link}" class="nav-btn">⬅️ Sebelumnya</a>
            <a href="{next_link}" class="nav-btn">Selanjutnya ➡️</a>
        </div>
        <a href="../index.html" class="back-index">Kembali ke Daftar Isi</a>
    </div>
</body>
</html>
"""
    with open(os.path.join(folder_output, nama_file), 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"Selesai! {total_pages} file HTML berprefix 'hj_' berhasil digenerate di folder bab_html.")
