@echo off

echo !=== COMPILING ===!
pyinstaller lnavHelp.py --onefile -i iconHlp.ico
pyinstaller main.py -i icon.ico --noconfirm
cd dist\main
rename main.exe lnav.exe
echo e >> lnavHelp.exe
cd ..
xcopy lnavHelp.exe main\lnavHelp.exe
cd ..
echo !=== FINISHED COMPILING ===!

echo !=== OPENING PROGRAM... ===!
cd dist/main
.\lnav.exe

pause