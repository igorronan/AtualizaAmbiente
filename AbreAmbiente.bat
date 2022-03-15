@echo off

TASKKILL /F /IM rm.host.exe /T
TASKKILL /F /IM rmSaude.exe /T
TASKKILL /F /IM rm.exe /T
TASKKILL /F /IM msedge.exe /T
net stop RM.Host.Service
cls

:Iniciando Variaveis
SET VAR=0
set folder_origin=%cd%

echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo . + Escoha a versao do RM a ser aberta
echo . + 2 Versao 12.1.32
echo . + 3 Versao 12.1.33
echo . + 4 Versao 12.1.34
echo . + 5 Versao 12.1.35
echo . +
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
CHOICE /C 2345 /M "Escolha uma das opcoes acima"


IF %ERRORLEVEL% EQU 1 goto rm2
IF %ERRORLEVEL% EQU 2 goto rm3
IF %ERRORLEVEL% EQU 3 goto rm4
IF %ERRORLEVEL% EQU 4 goto rm5
exit



:rm2
set /a v=32
set url=http://localhost/%v%
set pastasistema=C:\RM\Legado\12.1.32\Bin
goto AtualizaAmbiente

:rm3
set /a v=33
set url=http://localhost/%v%
set pastasistema=C:\RM\Legado\12.1.33\Bin
goto AtualizaAmbiente

:rm4
set /a v=34
set pastasistema=C:\RM\Legado\12.1.34\Bin
set url=http://localhost/%v%
goto AtualizaAmbiente

:rm5
set /a v=35
set url=http://localhost/atual
set pastasistema=C:\RM\Atual\Release\Bin
goto AtualizaAmbiente


:AtualizaAmbiente
cls
:Iniciando Atualização Sistema
call python3 "%folder_origin%\atualizador_novo.py" %v%


echo Abrindo host ...
start %pastasistema%\RM.Host.exe

:Aguardando Inicio Sistema
:loop

FOR /F "tokens=*" %%g IN ('cmd /c "python3 %folder_origin%\request.py http://localhost:8051/wsDataServer/MEX?wsdl"') do (SET VAR=%%g)
cls
echo Aguardando RM Hosts
if %VAR% EQU 1 (
goto iniciarRM
)
goto loop

:iniciarRM
start %pastasistema%\RM.exe

:Abrindo URL Sistema
"C:\Program Files\Google\Chrome\Application\chrome.exe" --app %url%


