@echo off
chcp 65001
cls
setlocal enabledelayedexpansion

set COMPILER=C:\msys64\ucrt64\bin\g++.exe

if not exist "%COMPILER%" (
    echo Ошибка: Компилятор не найден. Путь: %COMPILER%
    exit /b 1
)

if "%1"=="" (
    echo Ошибка: Не передан путь до файла компиляции.
    exit /b 1
)

if not exist "%1" (
    echo Ошибка: Файл "%1" не существует.
    exit /b 1
)


set OUTPUT=%CD%\%~n1.exe

:: Компиляция программы с сохранением ошибок в error.txt
"%COMPILER%" "%1" -o "%OUTPUT%" 2> error.txt

if errorlevel 1 (
    echo Ошибка компиляции. Подробнее в error.txt
    exit /b 1
) else (
    del error.txt >nul 2>nul
    echo Компиляция завершена. Запуск программы...
    "%OUTPUT%"
)

endlocal
