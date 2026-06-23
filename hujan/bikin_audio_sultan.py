import os
import glob
import struct
import time
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
# =====================================================================
# 🛠️ KONFIGURASI UTAMA (VERSI ROTASI 5 KUNCI SULTAN - START HALAMAN 6)
# =====================================================================
folder_html = "bab_html"         
folder_audio = "audio"           

# WAK, MASUKKAN KELIMA API KEY KAMU DI SINI:
API_KEYS = [
    
]

# Variabel pelacak sedang pakai key ke berapa
current_key_index = 0

if not os.path.exists(folder_audio):
    os.makedirs(folder_audio)

# =====================================================================
# 🤖 MESIN AUDIO SULTAN (ANTI-LIMIT / AUTO-SWITCHING)
# =====================================================================
def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    bits_per_sample = 16
    rate = 24000
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try: rate = int(param.split("=", 1)[1])
            except: pass
        elif param.startswith("audio/L"):
            try: bits_per_sample = int(param.split("L", 1)[1])
            except: pass

    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    sample_rate = rate
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size  

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1, num_channels,
        sample_rate, byte_rate, block_align, bits_per_sample, b"data", data_size
    )
    return header + audio_data

def generate_audio_for_page(file_path, output_path):
    global current_key_index
    print(f"\n📖 Membaca teks dari: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    daftar_paragraf = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]

    if not daftar_paragraf:
        print(f"⚠️  Skip {file_path}: Tidak ada teks paragraf ditemukan.")
        return True

    client = genai.Client(api_key=API_KEYS[current_key_index])
    audio_halaman_full = bytearray()
    mime_type_final = None

    print(f"🎙️  Menemukan {len(daftar_paragraf)} paragraf. Memproses dengan API Key ke-{current_key_index + 1}...")

    indeks = 0
    while indeks < len(daftar_paragraf):
        teks_p = daftar_paragraf[indeks]
        print(f"   └─ [{indeks + 1}/{len(daftar_paragraf)}] Merekam suara paragraf...")
        
        teks_siap_baca = f"Speaker 1: [warm] {teks_p}"
        instruksi_sutradara = f"""
        You are an expert audiobook director and narrator. 
        Analyze the following story text to detect its sub-genre (Sci-Fi, Romance, Drama, or Suspense) and overall emotional mood.
        Then, read the text as Speaker 1 using the most appropriate tone, expression, and pacing for that genre.
        
        ## Transcript:
        {teks_siap_baca}
        """

        contents = [types.Content(role="user", parts=[types.Part.from_text(text=instruksi_sutradara)])]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=0.7, 
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(speaker="Speaker 1", voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck"))),
                        types.SpeakerVoiceConfig(speaker="Speaker 2", voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr"))),
                    ]
                )
            ),
        )

        try:
            for chunk in client.models.generate_content_stream(
                model="gemini-3.1-flash-tts-preview",
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.parts is None: continue
                if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                    audio_halaman_full.extend(chunk.parts[0].inline_data.data)
                    if not mime_type_final:
                        mime_type_final = chunk.parts[0].inline_data.mime_type
            
            indeks += 1
            
        except Exception as e:
            pesan_error = str(e)
            if "429" in pesan_error or "RESOURCE_EXHAUSTED" in pesan_error or "Quota" in pesan_error:
                print(f"\n   ⚠️ [LIMIT HABIS] API Key ke-{current_key_index + 1} tewas!")
                current_key_index += 1
                
                if current_key_index >= len(API_KEYS):
                    print("   ❌ GAGAL TOTAL: Kelima stok API Key kamu sudah habis tak bersisa!")
                    return "HABIS_SEMUA"
                
                print(f"   🔄 GANTI MESIN: Pindah ke API Key ke-{current_key_index + 1}... Mengulang paragraf tadi.")
                client = genai.Client(api_key=API_KEYS[current_key_index])
                time.sleep(2)
            else:
                print(f"   ❌ Gagal di paragraf {indeks + 1} (Error tidak terduga): {pesan_error}")
                return False

    if audio_halaman_full:
        if not mime_type_final: mime_type_final = "audio/L16;rate=24000"
        wav_data = convert_to_wav(bytes(audio_halaman_full), mime_type_final)
        with open(output_path, "wb") as f:
            f.write(wav_data)
        print(f"✅ SUKSES UTUH: Audio disimpan di {output_path}")
        return True
    return False

# =====================================================================
# 🚀 EKSEKUSI BATCH (TEMBAK HALAMAN 6 SAMPAI KUNCI HABIS)
# =====================================================================
def main():
    jalur_pencarian = os.path.join(folder_html, "*.html")
    daftar_file = glob.glob(jalur_pencarian)
    daftar_file.sort()

    if not daftar_file:
        print(f"Folder '{folder_html}' kosong!")
        return

    # 🔥 MANTRA BARU: Mulai dari halaman 6 (Indeks 5) sampai array habis
    daftar_file = daftar_file[5:]
    print(f"⚡ Memulai penyerangan dari halaman 6 untuk {len(daftar_file)} halaman...\n")

    for file_html_path in daftar_file:
        nama_file = os.path.basename(file_html_path)
        nama_murni = os.path.splitext(nama_file)[0]
        
        nama_audio = f"audio_{nama_murni}_sultan_FULL.wav"
        file_audio_path = os.path.join(folder_audio, nama_audio)

        if os.path.exists(file_audio_path) and os.path.getsize(file_audio_path) > 0:
            print(f"⏭️  [SKIP] {nama_file} sudah memiliki audio valid.")
            continue
        elif os.path.exists(file_audio_path):
            print(f"🗑️  [REMAKE] Menemukan file kosong sisa crash pada {nama_file}, menimpa ulang...")

        status = generate_audio_for_page(file_html_path, file_audio_path)
        
        if status == "HABIS_SEMUA":
            print("\n🛑 PROGRAM BERHENTI. Seluruh 5 API Key sudah tumbang!")
            break

    print("\n🎉 BATCH TESTING SELESAI!")

if __name__ == "__main__":
    main()
