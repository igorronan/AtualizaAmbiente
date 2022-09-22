@setlocal enableextensions enabledelayedexpansion
@echo off
title Atualizador Totvs Restore

TASKKILL /F /IM rm.host.exe /T
TASKKILL /F /IM rmSaude.exe /T
TASKKILL /F /IM rm.exe /T
TASKKILL /F /IM RuntimeBroker.exe /T
net stop RM.Host.Service
cls

title VERIFICANDO EXISTENCIA DO PYTHON


where python
IF %ERRORLEVEL% EQU 0 (goto :PYTHON_DOES_EXIST)
IF %ERRORLEVEL% EQU 1 (goto :PYTHON_DOES_NOT_EXIST)
goto :fim



:PYTHON_DOES_NOT_EXIST
cls
color F4
title PYTHON NAO ENCONTRADO
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo . + 
echo . + 
echo . + VOCE DEVE REALIZAR A INSTALACAO DO PYTHON 3 PARA PROSSEGUIR
echo . +
echo . +
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
timeout -t 5 >nul
start "" "https://www.python.org/downloads/windows/"
exit
    


:PYTHON_DOES_EXIST
for /f "delims=" %%V in ('python -V') do @set ver=%%V
CLS
GOTO Iniciando


:Iniciando Variaveis
title ATUALIZADOR TOTVS RESTORE
SET VAR=0
set /A cont=1
set folder_origin=%~dp0
set versao=atual

echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo . + Escoha a versao do RM a ser aberta
echo . + Ex 2209
echo . + 
echo . + Para atual voce pode apenas apertar [ENTER]
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++

set /p versao="Versao: "

title Validando Versao
set aux="0"
set file=%folder_origin%\versoes.ini
set area=[%versao%]
set key=id
set currarea=
for /f "usebackq delims=" %%a in ("!file!") do (
    set ln=%%a
    if "x!ln:~0,1!"=="x[" (
        set currarea=!ln!
    ) else (
        for /f "tokens=1,2 delims==" %%b in ("!ln!") do (
            set currkey=%%b
            set currval=%%c
            if "x!area!"=="x!currarea!" if "x!key!"=="x!currkey!" (
                set aux="1"
            )
        )
    )
)


IF %AUX% EQU "0" (
    cls
    color F4
    title VERSAO NAO ENCONTRADA
    echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    echo . + 
    echo . + 
    echo . + A VERSAO DIGITADA NAO FOI ENCONTRADA NO ARQUIVO VERSOES.INI
    echo . +
    echo . +
    echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    timeout -t 7 >nul
    exit
)

IF [%versao%]==[atual] (
    SET local=atual
	SET versao=release
    SET v=atual
) ELSE (
    SET local=Legado
	set versao=12.1.%versao%
    set v=%versao%
)


set url=http://localhost/%v%
set pastasistema=C:\RM\%local%\%versao%

cls
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo . + Escoha a versao do RM a ser aberta
echo . + 1 SQL
echo . + 2 ORACLE
echo . +
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
CHOICE /C 12 /M "Escolha uma das opcoes acima"

IF %ERRORLEVEL% EQU 1 goto sql
IF %ERRORLEVEL% EQU 2 goto oracle
exit


:sql
set /a tipo=1
goto atualiza

:oracle
set /a tipo=2
goto atualiza
exit

:atualiza
cls
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo . + Escoha a versao do RM a ser aberta
echo . + 1 Atualizar Ambiente
echo . + 2 Apenas subir o Host
echo . +
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++
CHOICE /C 12 /M "Escolha uma das opcoes acima"


IF %ERRORLEVEL% EQU 1 goto segue
IF %ERRORLEVEL% EQU 2 goto host
exit

:segue
cls
title AGUARDE ATUALIZANDO VERSAO
call python3 "%folder_origin%\atualizador_novo.py" %v%
del %pastasistema%\Bin\_Broker.dat

:host
title AGUARDANDO INICIO DO RM.HOSTS.EXE
echo Aguardando RM Hosts
call python3 "%folder_origin%\alias.py" %v% %tipo% 
start %pastasistema%\Bin\RM.Host.exe

:loop
FOR /F "tokens=*" %%g IN ('cmd /c "python3 %folder_origin%\request.py http://localhost:8051/wsDataServer/MEX?wsdl"') do (SET VAR=%%g)
cls
set /A aux1=0
set progss=Aguardando RM Hosts 
:print

if %aux1% == %cont% ( goto endprint )
set /A aux1=aux1+1
set progss=%progss%X
goto print
:endprint
echo %progss%


if %VAR% EQU 1 (
goto criaSite
)
set /A cont=cont+1
goto loop

:criaSite
if exist "%pastasistema%\FrameHTML\web\app\Sau\PEP" "c:\Windows\System32\inetsrv\appcmd.exe" add app /site.name:"Default Web Site" /path:/%v% /physicalPath:"%pastasistema%\FrameHTML\web\app\Sau\PEP"


:iniciarRM
title INICIANDO RM
start %pastasistema%\Bin\RM.exe

:Abrindo URL Sistema
if exist "%pastasistema%\FrameHTML\web\app\Sau\PEP"  "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" --app %url%

cls
color 2F
title Processo Finalizado
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo . + 
echo . + 
echo . +            Versao atualizada com sucesso.
echo . +
echo . +
echo . ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
timeout -t 4 >nul