@echo off
if -%1 == - goto e1
if not exist *.txt goto e2
copy /b *.txt %1 > nul
del *.txt
echo Файл %1 создан!
goto exit

:e1
    echo Укажите имя результирующего файла!
    goto exit

:e2
    echo Нет файлов для объединения!
    goto exit

:exit
    pause
