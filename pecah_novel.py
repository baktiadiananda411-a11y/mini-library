import os
import re

file_ocr = "teks_mie_ayam.txt"
folder_output = "bab_html"

if not os.path.exists(folder_output):
    os.makedirs(folder_output)

with open(file_ocr, 'r', encoding='utf-8') as f:
    konten = f.read()

parts = re.split(r'---\s+halaman_(\d{3})\.webp\s+---', konten)

pages = []
for i in range(1, len(parts), 2):
    nomor_hal = parts[i]
    isi_hal = parts[i+1].strip()
    pages.append({"nomor": nomor_hal, "isi": isi_hal})

total_pages = len(pages)

# --- DAFTAR HALAMAN GAMBAR/ILUSTRASI ---
# Halaman 001 (Cover) sudah dimasukkan. 
halaman_gambar = [
    "001", "002", "004", "005", "007", "025", "037", 
    "051", "071", "091", "118", "119", "137", "159", 
    "177", "203", "204", "217"
]

for i, page in enumerate(pages):
    nomor = page['nomor']
    isi_mentah = page['isi']
    
    isi_rapi = '<p>' + isi_mentah.replace('\n\n', '</p><p>') + '</p>'
    isi_rapi = isi_rapi.replace('\n', ' ')
    
    nama_file = f"halaman_{nomor}.html"
    
    prev_link = f"halaman_{pages[i-1]['nomor']}.html" if i > 0 else "../index_mie_ayam.html"
    next_link = f"halaman_{pages[i+1]['nomor']}.html" if i < total_pages - 1 else "../index_mie_ayam.html"

    # --- LOGIKA PENYISIPAN GAMBAR ---
    if nomor in halaman_gambar:
        tag_gambar = f'<img src="../novel_mie_ayam/halaman_{nomor}.webp" alt="Ilustrasi Halaman {nomor}" class="page-img">'
        isi_rapi = "" # MENGHAPUS teks OCR agar hanya gambar yang tampil
    else:
        tag_gambar = ""

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halaman {nomor} - Seporsi Mie Ayam</title>
    <style>
        body {{
            background-color: #0f0f0f; color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8; margin: 0; padding: 20px;
            transition: background-color 0.3s, color 0.3s;
        }}
        .container {{
            max-width: 800px; margin: 40px auto;
            background-color: #1e1e1e; padding: 40px;
            border-radius: 12px; box-shadow: 0 12px 25px rgba(187, 134, 252, 0.05);
            border: 1px solid #333; transition: background-color 0.3s, border-color 0.3s;
        }}
        h1 {{
            color: #555; text-align: center; margin-bottom: 20px;
            font-size: 1.2em; letter-spacing: 2px; border-bottom: 1px dashed #333;
            padding-bottom: 15px; text-transform: uppercase;
        }}
        p {{ margin-bottom: 20px; font-size: 1.1em; text-align: justify; color: #ccc; }}
        
        .page-img {{
            display: block; max-width: 100%; height: auto;
            margin: 0 auto 30px auto; border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5); border: 1px solid #444;
        }}

        .nav-buttons {{ display: flex; justify-content: space-between; margin: 30px 0; }}
        .nav-btn {{
            background-color: #2c2c2c; color: #bb86fc; padding: 10px 20px;
            text-decoration: none; border-radius: 6px; font-weight: bold;
            transition: all 0.2s; border: 1px solid #bb86fc;
        }}
        .nav-btn:hover {{ background-color: #bb86fc; color: #121212; }}
        .back-index {{
            display: block; text-align: center; margin-top: 40px; color: #888;
            text-decoration: none; font-size: 0.9em; transition: color 0.2s;
        }}
        .back-index:hover {{ color: #bb86fc; }}

        /* TEMA TERANG */
        body.light-mode {{ background-color: #f4f4f4; color: #333; }}
        body.light-mode .container {{ background-color: #ffffff; border-color: #ddd; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
        body.light-mode h1 {{ color: #5e35b1; border-bottom-color: #ddd; }}
        body.light-mode p {{ color: #222; }}
        body.light-mode .nav-btn {{ background-color: #ffffff; color: #5e35b1; border-color: #5e35b1; }}
        body.light-mode .nav-btn:hover {{ background-color: #5e35b1; color: #ffffff; }}
        body.light-mode .back-index {{ color: #5e35b1; }}
        body.light-mode .back-index:hover {{ color: #4527a0; }}
        body.light-mode .page-img {{ border-color: #ccc; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}

        .theme-toggle {{
            position: fixed; top: 20px; right: 20px; background: #bb86fc; color: #121212; 
            border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; 
            font-weight: bold; z-index: 1000; transition: 0.3s;
        }}
        body.light-mode .theme-toggle {{ background: #5e35b1; color: #fff; }}
        
        @media (max-width: 600px) {{
            .container {{ padding: 20px; margin: 10px auto; }}
            .nav-btn {{ padding: 8px 15px; font-size: 0.9em; }}
        }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Ubah Tema</button>
    <script>
        function toggleTheme() {{ document.body.classList.toggle('light-mode'); }}
    </script>

    <div class="container">
        <h1>Halaman {nomor}</h1>
        
        {tag_gambar}
        <div>{isi_rapi}</div>
        
        <div class="nav-buttons">
            <a href="{prev_link}" class="nav-btn">⬅️ Hal Sebelumnya</a>
            <a href="{next_link}" class="nav-btn">Hal Selanjutnya ➡️</a>
        </div>
        
        <a href="../index_mie_ayam.html" class="back-index">Kembali ke Daftar Isi</a>
    </div>
</body>
</html>
"""
    with open(os.path.join(folder_output, nama_file), 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"Selesai! Halaman gambar (seperti cover 001) sekarang HANYA menampilkan gambar tanpa teks berantakan.")
