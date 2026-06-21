import os
import glob

# Konfigurasi
folder_gambar = "novel_gambar"
folder_output = "bab_html"
prefix = "rs_" # Prefix khusus
judul_novel = "Ruang Sunyi Bernama Kamu"

if not os.path.exists(folder_output):
    os.makedirs(folder_output)

list_gambar = sorted(glob.glob(f"{folder_gambar}/halaman_*.jpg"))

if not list_gambar:
    print("Gambar tidak ditemukan! Pastikan hasil ekstrak ada di folder novel_gambar.")
    exit()

pages = []
for path in list_gambar:
    nama_file_gambar = os.path.basename(path)
    nomor = nama_file_gambar.replace("halaman_", "").replace(".jpg", "")
    pages.append({"nomor": nomor, "file_gambar": nama_file_gambar})

total_pages = len(pages)

# --- 1. MEMBUAT HALAMAN BACA ---
for i, page in enumerate(pages):
    nomor = page['nomor']
    file_gambar = page['file_gambar']
    
    nama_file_html = f"{prefix}halaman_{nomor}.html"
    
    prev_link = f"{prefix}halaman_{pages[i-1]['nomor']}.html" if i > 0 else "../index.html"
    next_link = f"{prefix}halaman_{pages[i+1]['nomor']}.html" if i < total_pages - 1 else "../index.html"

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halaman {nomor} - {judul_novel}</title>
    <style>
        body {{ background-color: #0f0f0f; color: #e0e0e0; font-family: sans-serif; margin: 0; padding: 20px; transition: 0.3s; display: flex; flex-direction: column; align-items: center; }}
        .container {{ width: 100%; max-width: 700px; background-color: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333; }}
        .page-img {{ display: block; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        .nav-buttons {{ display: flex; justify-content: space-between; margin-top: 30px; }}
        .nav-btn {{ background-color: #2c2c2c; color: #bb86fc; padding: 12px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; border: 1px solid #bb86fc; }}
        .back-index {{ display: block; text-align: center; margin-top: 30px; color: #888; text-decoration: none; }}
        
        body.light-mode {{ background-color: #f4f4f4; }}
        body.light-mode .container {{ background-color: #fff; border-color: #ddd; }}
        body.light-mode .nav-btn {{ background-color: #fff; color: #5e35b1; border-color: #5e35b1; }}
        .theme-toggle {{ position: fixed; top: 20px; right: 20px; background: #bb86fc; color: #121212; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold; }}
        body.light-mode .theme-toggle {{ background: #5e35b1; color: #fff; }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Tema</button>
    <script>
        function toggleTheme() {{ document.body.classList.toggle('light-mode'); }}
        document.addEventListener("DOMContentLoaded", function() {{
            let currentFile = "{nama_file_html}";
            localStorage.setItem('rs_last_read', currentFile);
            let riwayatBaca = JSON.parse(localStorage.getItem('rs_read_pages') || '[]');
            if (!riwayatBaca.includes(currentFile)) {{
                riwayatBaca.push(currentFile);
                localStorage.setItem('rs_read_pages', JSON.stringify(riwayatBaca));
            }}
        }});
    </script>
    <div class="container">
        <img src="../{folder_gambar}/{file_gambar}" alt="Halaman {nomor}" class="page-img">
        <div class="nav-buttons">
            <a href="{prev_link}" class="nav-btn">⬅️ Prev</a>
            <a href="{next_link}" class="nav-btn">Next ➡️</a>
        </div>
        <a href="../index.html" class="back-index">Kembali ke Daftar Isi</a>
    </div>
</body>
</html>
"""
    with open(os.path.join(folder_output, nama_file_html), 'w', encoding='utf-8') as f:
        f.write(html_content)

# --- 2. MEMBUAT DAFTAR ISI ---
index_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{judul_novel} - Daftar Isi</title>
    <style>
        body {{ background-color: #121212; color: #e0e0e0; font-family: sans-serif; display: flex; justify-content: center; padding: 20px; transition: 0.3s; }}
        .wrapper {{ width: 100%; max-width: 600px; text-align: center; padding-top: 20px; }}
        h1 {{ color: #bb86fc; margin-bottom: 5px; }}
        .btn-kembali {{ color: #bb86fc; text-decoration: none; font-weight: bold; display: block; margin-bottom: 20px; }}
        .btn-lanjut {{ display: none; background: #bb86fc; color: #121212; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; margin: 20px auto; max-width: 250px; }}
        .grid-daftar {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; padding: 0; list-style: none; margin-top: 20px; }}
        .grid-daftar a {{ background: #2c2c2c; color: #bb86fc; text-decoration: none; padding: 10px; border-radius: 6px; border: 1px solid #3d3d3d; display: block; position: relative; font-weight: bold; font-size: 14px; }}
        .grid-daftar a.sudah-dibaca::after {{ content: ""; position: absolute; top: 5px; right: 5px; width: 8px; height: 8px; background-color: #ff4c4c; border-radius: 50%; }}
        
        body.light-mode {{ background-color: #f4f4f4; color: #333; }}
        body.light-mode .grid-daftar a {{ background: #fff; color: #5e35b1; border-color: #ddd; }}
        body.light-mode .btn-lanjut {{ background: #5e35b1; color: #fff; }}
        .theme-toggle {{ position: fixed; top: 20px; right: 20px; background: #bb86fc; color: #121212; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold; }}
        body.light-mode .theme-toggle {{ background: #5e35b1; color: #fff; }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Tema</button>
    <div class="wrapper">
        <a href="../index.html" class="btn-kembali">← Lobi Utama</a>
        <h1>{judul_novel}</h1>
        <p style="color:#888;">Format Visual</p>
        <a href="#" id="btnLanjut" class="btn-lanjut">📖 Lanjut Membaca</a>
        <ul class="grid-daftar">
"""

for page in pages:
    index_html += f'            <li><a href="{folder_output}/{prefix}halaman_{page["nomor"]}.html">Hal {page["nomor"]}</a></li>\n'

index_html += """        </ul>
    </div>
    <script>
        function toggleTheme() { document.body.classList.toggle('light-mode'); }
        document.addEventListener("DOMContentLoaded", function() {
            let lastRead = localStorage.getItem('rs_last_read');
            if (lastRead) {
                let btn = document.getElementById('btnLanjut');
                btn.href = "bab_html/" + lastRead;
                btn.style.display = "block";
            }
            let riwayatBaca = JSON.parse(localStorage.getItem('rs_read_pages') || '[]');
            riwayatBaca.forEach(function(pageFile) {
                let kotakLink = document.querySelector('.grid-daftar a[href="bab_html/' + pageFile + '"]');
                if (kotakLink) kotakLink.classList.add('sudah-dibaca');
            });
        });
    </script>
</body>
</html>
"""

with open("index.html", 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"Selesai! {total_pages} halaman HTML berhasil digenerate untuk Ruang Sunyi Bernama Kamu.")
