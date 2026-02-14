import psutil
import time
import os
import sys

# ===== ŚCIEŻKA BAZOWA =====
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PLIK_UNLOCK = os.path.join(BASE_DIR, "unlock.flag")
CONFIG_GLOWNY = os.path.join(BASE_DIR, "config2.txt")
CONFIG_DODATKOWY = os.path.join(BASE_DIR, "extraprc.txt")

# ===== GŁÓWNY PROCES (INICJALIZACJA!) =====
GLOWNY_PROCES = None

if os.path.exists(CONFIG_GLOWNY):
    with open(CONFIG_GLOWNY, "r", encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if linia.startswith("PROCES="):
                GLOWNY_PROCES = linia.split("=", 1)[1]

if not GLOWNY_PROCES:
    print("error: no PROCES= w config2.txt")
    input("Press enter to exit...")
    sys.exit(1)

# ===== DODATKOWE PROCESY (MAX 5) =====
DODATKOWE_PROCESY = []

if os.path.exists(CONFIG_DODATKOWY):
    with open(CONFIG_DODATKOWY, "r", encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if linia and len(DODATKOWE_PROCESY) < 5:
                DODATKOWE_PROCESY.append(linia)

# ===== LISTA WSZYSTKICH PROCESÓW =====
WSZYSTKIE_PROCESY = [GLOWNY_PROCES] + DODATKOWE_PROCESY
print("Guard")
print("by Fraknek")
print(" ")
print("Guard Running")
print("Secured Processes:")
for p in WSZYSTKIE_PROCESY:
    print(" -", p)

# ===== FUNKCJE =====
def proces_dziala(nazwa):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == nazwa:
                return True
        except psutil.NoSuchProcess:
            pass
    return False

def zamknij_proces(nazwa):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == nazwa:
                proc.kill()
        except psutil.NoSuchProcess:
            pass

# ===== STANY POPRZEDNIE =====
poprzedni_stan = {p: False for p in WSZYSTKIE_PROCESY}

# ===== PĘTLA GŁÓWNA =====
while True:
    unlock_istnieje = os.path.exists(PLIK_UNLOCK)

    for proces in WSZYSTKIE_PROCESY:
        dziala = proces_dziala(proces)

        # 🔴 brak unlock.flag → zamykaj
        if not unlock_istnieje and dziala:
            zamknij_proces(proces)

        # 🟢 proces się zamknął → usuń unlock.flag
        if poprzedni_stan[proces] and not dziala:
            if os.path.exists(PLIK_UNLOCK):
                try:
                    os.remove(PLIK_UNLOCK)
                except Exception as e:
                    print("Error while deleting unlock.flag file:", e)

        poprzedni_stan[proces] = dziala

    time.sleep(0.5)
