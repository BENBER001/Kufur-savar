"""
Clean Rap Muter v2
----------------
Sadece küfür olan kelimenin tam zamanını tahmin eder ve o anlık sesi kısar.
Kök eşleştirme mantığıyla çalışır (örn: piç -> piçin, piçe hepsini yakalar).
"""

import os
import re
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

try:
    import syncedlyrics
except ImportError:
    syncedlyrics = None

# --------------------------------------------------------------------------
# AYARLAR
# --------------------------------------------------------------------------

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "buraya_yazcan")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "buraya_yazcan")
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

BLACKLIST_FILE = "blacklist.txt"

POLL_INTERVAL_SECONDS = 0.15     
LOOKAHEAD_MS = 50                
LINE_END_BUFFER_MS = 50          
MUTE_VOLUME = 0                  
NORMAL_VOLUME = None              

# --------------------------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# --------------------------------------------------------------------------

TR_LOWER_MAP = str.maketrans({
    "İ": "i", "I": "ı", "Ç": "ç", "Ğ": "ğ", "Ö": "ö", "Ş": "ş", "Ü": "ü",
})

def normalize(text: str) -> str:
    text = text.translate(TR_LOWER_MAP).lower()
    text = re.sub(r"[^a-z0-9çğıöşü\s]", " ", text)
    return text

def load_blacklist(path: str) -> set:
    if not os.path.exists(path):
        print(f"[UYARI] {path} bulunamadı, boş kara liste ile devam ediliyor.")
        return set()
    with open(path, "r", encoding="utf-8") as f:
        words = {normalize(line.strip()) for line in f if line.strip()}
    return words

def is_bad_word(word: str, blacklist: set) -> bool:
    """
    Kelime birebir listede var mı VEYA listedeki bir kelimeyle başlıyor mu diye bakar.
    3 harften kısa kelimelerde (örn: am) hatalı eşleşmeyi (ama) önlemek için
    sadece birebir eşleşme aranır.
    """
    norm_word = normalize(word).strip()
    if not norm_word:
        return False
        
    for bad in blacklist:
        if norm_word == bad:
            return True
        # Ek almış hallerini yakalamak için (piç -> piçin, piçti)
        if len(bad) >= 3 and norm_word.startswith(bad):
            return True
    return False

def parse_lrc(lrc_text: str):
    pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
    lines = []
    for raw_line in lrc_text.splitlines():
        m = pattern.match(raw_line.strip())
        if not m:
            continue
        minutes, seconds, text = m.groups()
        start_ms = int((int(minutes) * 60 + float(seconds)) * 1000)
        text = text.strip()
        if text:
            lines.append([start_ms, None, text])

    lines.sort(key=lambda x: x[0])
    for i in range(len(lines) - 1):
        lines[i][1] = lines[i + 1][0]
    if lines:
        lines[-1][1] = lines[-1][0] + 5000 

    return lines

def fetch_flagged_intervals(track_name: str, artist_name: str, blacklist: set):
    """
    LRC sözlerini indirir ve SADECE küfürlü kelimelerin tahmini
    başlangıç ve bitiş zamanlarını hesaplar.
    """
    if syncedlyrics is None:
        print("[UYARI] syncedlyrics kurulu değil, söz analizi atlanıyor.")
        return []

    query = f"{track_name} {artist_name}"
    try:
        lrc_text = syncedlyrics.search(query, synced_only=True, providers=["Lrclib", "NetEase", "Megalobiz"])
    except Exception as e:
        print(f"[UYARI] Söz bulunamadı ({query}): {e}")
        return None

    if not lrc_text:
        print(f"[UYARI] '{query}' için senkronize söz bulunamadı.")
        return None

    lines = parse_lrc(lrc_text)
    flagged = []
    
    for start, end, text in lines:
        if not end:
            end = start + 5000
            
        words = text.split()
        if not words:
            continue
            
        # Satırın süresini hesapla ve karakter başına düşen milisaniyeyi bul
        line_duration = end - start
        total_chars = max(len(text), 1)
        char_time = line_duration / total_chars
        
        current_char_pos = 0
        for w in words:
            clean_w = normalize(w).strip()
            if clean_w and is_bad_word(clean_w, blacklist):
                # Kelimenin satırdaki konumuna göre zaman aralığını hesapla
                w_start = start + int(current_char_pos * char_time)
                w_end = start + int((current_char_pos + len(w)) * char_time)
                
                # Kelimenin sesi anında açıp kapaması için ufak esneme payı ekliyoruz
                flagged.append((w_start, w_end))
                print(f"    [YAKALANDI] {w_start/1000:.1f}sn - {w_end/1000:.1f}sn: \"{w}\"")
            
            # Boşluk karakterini de hesaba kat
            current_char_pos += len(w) + 1 

    print(f"[BİLGİ] '{track_name}' içinde {len(flagged)} küfürlü kelime bulundu.")
    return flagged

# --------------------------------------------------------------------------
# ANA DÖNGÜ
# --------------------------------------------------------------------------

def main():
    blacklist = load_blacklist(BLACKLIST_FILE)
    print(f"[BİLGİ] Kara listede {len(blacklist)} kelime yüklendi.")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="user-read-playback-state user-modify-playback-state user-read-currently-playing",
    ))

    current_track_id = None
    flagged_intervals = []
    is_muted = False
    saved_volume = 70 

    print("[BİLGİ] Başlatıldı. Spotify'da müzik çalmaya başla...")

    while True:
        try:
            playback = sp.current_playback()
        except Exception as e:
            print(f"[HATA] Spotify API isteği başarısız: {e}")
            time.sleep(2)
            continue

        if not playback or not playback.get("is_playing"):
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        track = playback["item"]
        track_id = track["id"]
        position_ms = playback["progress_ms"]
        device_volume = playback["device"]["volume_percent"]

        if not is_muted:
            saved_volume = device_volume

        if track_id != current_track_id:
            current_track_id = track_id
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            print(f"\n[BİLGİ] Şimdi çalıyor: {artist_name} - {track_name}")
            flagged_intervals = fetch_flagged_intervals(track_name, artist_name, blacklist) or []
            is_muted = False

        should_mute = any(
            (start - LOOKAHEAD_MS) <= position_ms <= (end + LINE_END_BUFFER_MS)
            for start, end in flagged_intervals
        )

        if should_mute and not is_muted:
            try:
                sp.volume(MUTE_VOLUME)
                is_muted = True
                # Milisaniye detayı loglandı
                print(f"[SES KISILDI] {position_ms/1000:.2f} sn") 
            except Exception as e:
                print(f"[HATA] Ses kısılamadı: {e}")

        elif not should_mute and is_muted:
            try:
                target = NORMAL_VOLUME if NORMAL_VOLUME is not None else saved_volume
                sp.volume(target)
                is_muted = False
                print(f"[SES AÇILDI] {position_ms/1000:.2f} sn")
            except Exception as e:
                print(f"[HATA] Ses açılamadı: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()