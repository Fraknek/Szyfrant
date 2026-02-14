import customtkinter
import tkinter.messagebox
import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PLIK_CONFIG = os.path.join(BASE_DIR, "config.txt")
PLIK_ODBLOCKOWANIA = os.path.join(BASE_DIR, "unlock.flag")

if not os.path.exists(PLIK_CONFIG):
    tkinter.messagebox.showerror("No config", "No file named config.txt")
    #input("Press Enter to close")
    sys.exit(1)

HASLO = None
with open(PLIK_CONFIG, "r", encoding="utf-8") as f:
    for linia in f:
        if linia.startswith("HASLO="):
            HASLO = linia.strip().split("=", 1)[1]

if not HASLO:
    tkinter.messagebox.showerror("Edit your config", "Nothing typed after HASLO= in config.txt")
    #input("Press Enter to close")
    sys.exit(1)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x200")
root.title("Szyfrant")

customtkinter.CTkLabel(
    root,
    text="Szyfrant by Fraknek",
    font=customtkinter.CTkFont(size=30),
    text_color="orange"
).pack(pady=10)

entry = customtkinter.CTkEntry(
    root,
    width=150,
    placeholder_text="Password",
    show="*"
)
entry.pack(pady=20)

def sprawdzhaslo():

    if entry.get() == HASLO:
        with open(PLIK_ODBLOCKOWANIA, "w", encoding="utf-8") as f:
            f.write("kk")
            root.destroy()
    else:
        tkinter.messagebox.showinfo("Wrong Password", "Wrong Password, try again")

customtkinter.CTkButton(
    root,
    text="Enter",
    command=sprawdzhaslo
).pack(pady=10)

root.mainloop()

