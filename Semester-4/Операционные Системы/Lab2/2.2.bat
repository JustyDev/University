
@echo off
chcp 1251 > nul
setlocal EnableDelayedExpansion

REM Проверка количества аргументов
if "%~2"=="" (
    echo Ошибка: Недостаточно параметров.
    echo Использование: %~n0 имя_текстового_файла сообщение
    exit /b 1
)

REM Сохраняем аргументы в переменные
set "file_name=%~1"
set "message=%~2"

REM Проверяем, что сообщение состоит из одного слова (нет пробелов)
echo %message%| findstr /C:" " >nul
if not errorlevel 1 (
    echo Ошибка: Сообщение должно состоять из одного слова.
    exit /b 1
)

REM Создаем текстовый файл с сообщением
echo %message%> "%file_name%"
echo Файл '%file_name%' создан с сообщением '%message%'.

REM Проверяем наличие файла report.txt
if not exist report.txt (
    echo Файл 'report.txt' не существует. Создаю новый файл.
    type nul > report.txt
)

REM Добавляем сообщение в файл report.txt
echo %message%>> report.txt
echo Сообщение '%message%' добавлено в файл 'report.txt'.

exit /b 0
