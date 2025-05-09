$folderPath = Read-Host "Enter the folder path"

if (Test-Path $folderPath) {
    $files = Get-ChildItem -Path $folderPath -File

    $currentDate = Get-Date

    # Перебираем файлы
    foreach ($file in $files) {
        if (($currentDate - $file.LastWriteTime).Days -gt 7) {
            Remove-Item -Path $file.FullName -Force
            Write-Host "File '$($file.Name)' deleted."
        }
    }

    Write-Host "Finished checking files."
}
else {
    Write-Host "The folder '$folderPath' does not exist."
}
