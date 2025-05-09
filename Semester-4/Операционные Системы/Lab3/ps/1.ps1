[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

$apps = Get-AppxPackage | Select-Object Name, PackageFullName

# Показываем список приложений с нумерацией
Write-Host "List of installed apps:"
for ($i = 0; $i -lt $apps.Count; $i++) {
    Write-Host "$i. $($apps[$i].Name)"
}

[int]$choice = Read-Host "Enter the number of the application you want to delete"

# Проверка корректности ввода
if ($choice -ge 0 -and $choice -lt $apps.Count) {
    $selectedApp = $apps[$choice]
    Write-Host "`nDeletion: $($selectedApp.Name)`n"

    # Удаление выбранного приложения
    Get-AppxPackage -Name $selectedApp.Name | Remove-AppxPackage

    Write-Host "`nApplication is deleted."
} else {
    Write-Host "`nWrong enter. Closing of script."
}
