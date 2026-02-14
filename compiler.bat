@echo off
title Compiler

:start
echo Compiler
echo by Fraknek
python -m PyInstaller --onefile --icon=klucz.ico --noconsole szyfrant_v2.py
echo Gotowe
pause