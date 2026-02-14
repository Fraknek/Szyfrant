import os
import sys

print("Szyfrant")
print("by Fraknek")

# ===== ŚCIEŻKA DZIAŁAJĄCA W PY + EXE =====
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PLIK_CONFIG = os.path.join(BASE_DIR, "config1.txt")
PLIK_ODBLOCKOWANIA = os.path.join(BASE_DIR, "unlock.flag")

# ===== SPRAWDZENIE CONFIGU =====
if not os.path.exists(PLIK_CONFIG):
    print("❌ No config1.txt file")
    input("Press Enter to close")
    sys.exit(1)

# ===== WCZYTAJ HASŁO =====
HASLO = None
with open(PLIK_CONFIG, "r", encoding="utf-8") as f:
    for linia in f:
        if linia.startswith("HASLO="):
            HASLO = linia.strip().split("=", 1)[1]

if not HASLO:
    print("❌ no HASLO= in config1.txt")
    input("Press Enter to close")
    sys.exit(1)

# ===== PĘTLA HASŁA =====
while True:
    podane = input("Type Password: ")

    if podane == HASLO:
        with open(PLIK_ODBLOCKOWANIA, "w") as f:
            f.write("KK")
        print("👍")
        break
    else:
        print("Wrong Password, try again\n")
