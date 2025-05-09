@echo off
chcp 65001
cls
setlocal DisableDelayedExpansion

set COMPILER=C:\msys64\ucrt64\bin\g++.exe

if not exist "%COMPILER%" (
    echo Ошибка: Компилятор g++ не найден по пути %COMPILER%
    exit /b 1
)

if "%1"=="" (
    echo Ошибка: Не указан файл для компиляции.
    exit /b 1
)

if not exist "%1" (
    echo Ошибка: Файл "%1" не найден.
    exit /b 1
)

:menu
cls
echo ================================
echo      Виртуальный Компилятор
echo ================================
color 07

ask.exe
set RESULT=%errorlevel%

if %RESULT%==3 goto exit
if %RESULT%==2 goto edit
if %RESULT%==1 goto compile

color 0C
echo [!] Неверный выбор. Повторите попытку.
pause
goto menu

:compile
echo.
echo Запущена компиляция...
set OUTPUT=%CD%\%~n1.exe

REM Компиляция программы с сохранением ошибок в error.txt
"%COMPILER%" "%1" -o "%OUTPUT%" 2> dialog_error.txt

if errorlevel 1 (
    echo Ошибка при компиляции. Подробнее см. в dialog_error.txt
    exit /b 1
) else (
    del dialog_error.txt >nul 2>nul
    echo Компиляция успешна. Запуск программы...
    "%OUTPUT%"
)
goto menu

:edit
echo.
echo Открытие "%1" в C++ Builder...
code "%1"
goto menu

:exit
echo Завершение программы...
timeout /t 1 >nul
exit /b 1

endlocal