@echo off

echo !=== COMPILING ===!
pyinstaller main.py -i icon.ico --noconfirm
cd dist\main
rename main.exe lnav.exe
cd ..
cd ..
echo !=== FINISHED COMPILING ===!

echo !=== OPENING PROGRAM... ===!
cd dist/main
.\lnav.exe

pause