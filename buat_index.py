import os
import re

folder_output = "bab_html"
nama_file_index = "index_mie_ayam.html"

# Mengambil file halaman dan mengurutkannya
files = sorted([f for f in os.listdir(folder_output) if f.startswith('halaman_') and f.endswith('.html')], 
               key=lambda x: int(re.search(r'\d+', x).group()))

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seporsi Mie Ayam Sebelum Mati - Daftar Isi</title>
    <style>
        /* --- TEMA GELAP (DEFAULT) --- */
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            transition: background-color 0.3s, color 0.3s;
        }
        .main-container {
            width: 100%;
            max-width: 450px;
            text-align: center;
            padding-top: 40px;
        }
        h1 { color: #bb86fc; font-size: 24px; margin-bottom: 10px; transition: color 0.3s; }
        .subtitle { color: #888; font-style: italic; margin-bottom: 30px; }
        .back-link { color: #bb86fc; text-decoration: none; display: block; margin-bottom: 30px; font-weight: bold; transition: color 0.3s; }
        .page-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .page-btn {
            background-color: #2c2c2c; color: #bb86fc; text-decoration: none; padding: 15px;
            border-radius: 8px; font-weight: bold; transition: all 0.3s; border: 1px solid #333;
        }
        .page-btn:hover { background-color: #3d3d3d; border-color: #bb86fc; }

        /* --- TEMA TERANG (LIGHT MODE) --- */
        body.light-mode { background-color: #f4f4f4; color: #333; }
        body.light-mode .page-btn { background-color: #ffffff; color: #5e35b1; border-color: #ddd; }
        body.light-mode .page-btn:hover { background-color: #eaeaea; border-color: #5e35b1; }
        body.light-mode h1, body.light-mode .back-link { color: #5e35b1; }
        
        /* --- TOMBOL SAKLAR TEMA --- */
        .theme-toggle {
            position: fixed; top: 20px; right: 20px; background: #bb86fc; color: #121212; 
            border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; 
            font-weight: bold; z-index: 1000; transition: 0.3s;
        }
        body.light-mode .theme-toggle { background: #5e35b1; color: #fff; }
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Ubah Tema</button>
    <script>
        function toggleTheme() {
            document.body.classList.toggle('light-mode');
        }
    </script>

    <div class="main-container">
        <a href="index.html" class="back-link">← Kembali ke Library Utama</a>
        <h1>Seporsi Mie Ayam<br>Sebelum Mati</h1>
        <p class="subtitle">Koleksi Halaman Digital</p>
        
        <div class="page-grid">
"""

for f in files:
    nomor = re.search(r'\d+', f).group()
    nomor_tampil = str(int(nomor))
    html_content += f'            <a href="{folder_output}/{f}" class="page-btn">Halaman {nomor_tampil.zfill(3)}</a>\n'

html_content += """        </div>
    </div>
</body>
</html>
"""

with open(nama_file_index, "w", encoding='utf-8') as f:
    f.write(html_content)

print(f"Berhasil! {nama_file_index} sudah diperbarui dengan tombol saklar tema gelap/terang.")
