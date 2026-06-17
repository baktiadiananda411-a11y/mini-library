from PIL import Image
import os

def jadikan_siluet_transparan(file_asal, file_tujuan):
    if not os.path.exists(file_asal):
        print(f"[X] File {file_asal} tidak ditemukan di folder ini.")
        return

    try:
        # Buka gambar dan ubah ke mode RGBA (Red, Green, Blue, Alpha/Transparan)
        img = Image.open(file_asal)
        img = img.convert("RGBA")
        data = img.getdata()

        data_baru = []
        for pixel in data:
            # Jika piksel berwarna putih atau mendekati putih (latar belakang)
            if pixel[0] > 220 and pixel[1] > 220 and pixel[2] > 220:
                # Jadikan transparan (Alpha = 0)
                data_baru.append((255, 255, 255, 0))
            else:
                # Ubah gambar utamanya menjadi siluet abu-abu sangat gelap
                data_baru.append((25, 25, 25, 255))

        img.putdata(data_baru)
        
        # Simpan langsung ke folder malioboro
        img.save(file_tujuan, "PNG")
        print(f"[V] Berhasil membuat {file_tujuan}!")
    except Exception as e:
        print(f"[X] Gagal memproses {file_asal}: {e}")

# Eksekusi pembuatan siluet
print("Memulai proses manipulasi gambar...")
jadikan_siluet_transparan("Untitled.jpg", "malioboro/siluet_tugu.png")
jadikan_siluet_transparan("Untitled2.jpg", "malioboro/siluet_lampu.png")
