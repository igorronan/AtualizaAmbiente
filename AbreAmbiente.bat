@echo off
TASKKILL /F /IM rm.host.exe /T
TASKKILL /F /IM rmSaude.exe /T
TASKKILL /F /IM rm.exe /T
net stop RM.Host.Service
cls
set folder_origin=%cd%

echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo . + Escoha a versao do RM a ser aberta
echo . + 2 Versao 12.1.32
echo . + 3 Versao 12.1.33
echo . + 4 Versao 12.1.34
echo . + 5 Versao 12.1.35
echo . +
echo . + 0 Sair
echo . + a Fechar RM

CHOICE /C 23450a /M "Escolha uma das opcoes acima"


IF %ERRORLEVEL% EQU 1 goto rm2
IF %ERRORLEVEL% EQU 2 goto rm3
IF %ERRORLEVEL% EQU 3 goto rm4
IF %ERRORLEVEL% EQU 4 goto rm5
goto fim



:rm2
set /a v=32
set url=http://localhost/%v%
cd C:\RM\Legado\12.1.32\Bin
goto fechar

:rm3
set /a v=33
set url=http://localhost/%v%
cd C:\RM\Legado\12.1.33\Bin
goto fechar

:rm4
set /a v=34
cd C:\RM\Legado\12.1.34\Bin
set url=http://localhost/%v%
goto fechar

:rm5
set /a v=35
set url=http://localhost/atual
cd C:\RM\Atual\Release\Bin
goto fechar


:fechar
cls
call python3 "%folder_origin%\atualizador.py" %v%
echo Abrindo host ...
start RM.Host.exe
timeout /t 10 > nul
start RM.exe

"C:\Program Files\Google\Chrome\Application\chrome.exe" %url%

:fim
timeout -t 3 > nul