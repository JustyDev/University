# Thresholds
$cpuThreshold = 10  # Минимальная загрузка CPU для отображения
$ramThreshold = 50MB  # Минимальная память для отображения

# Получение всех процессов без системных
$allProcesses = Get-Process | Where-Object {
    $_.ProcessName -notin @('Idle', 'System', 'smss')
} 

# Фильтрация по владельцу с обработкой ошибок
$filteredProcesses = @()

foreach ($proc in $allProcesses) {
    try {
        $owner = (Get-WmiObject Win32_Process -Filter "ProcessId = $($proc.Id)" | Select-Object -ExpandProperty GetOwner -ErrorAction Stop)
        
        # Проверка владельца, исключение системных пользователей
        if ($owner -and $owner.User -notin @('SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE')) {
            $filteredProcesses += $proc
        }
    } catch {
        # Игнорирование процессов, к которым нет доступа
        continue
    }
}


# Фильтр по потреблению ресурсов
$filteredProcesses = $allProcesses | Where-Object {
    $_.CPU -le $cpuThreshold -or $_.WorkingSet64 -le $ramThreshold
} | Sort-Object CPU -Descending

# Вывод информации
if ($filteredProcesses) {
    Write-Host "Active Processes Consuming Resources:" -ForegroundColor Yellow
    $filteredProcesses | Select-Object ProcessName, Id, CPU, 
        @{Name="RAM (MB)"; Expression={($_.WorkingSet64 / 1MB).ToString("0.00")}} |
        Format-Table -AutoSize
} else {
    Write-Host "No resource-consuming processes found." -ForegroundColor Cyan
    Exit
}

# Выбор процессов для завершения
Write-Host "`nEnter the ID(s) of the processes to terminate (comma or space separated):" -ForegroundColor Magenta
$userInput = Read-Host "Process ID(s)"

# Проверка и завершение процессов
if ($userInput) {
    # Разделение строк на массив ID
    $processIds = $userInput -split '[, ]+' | ForEach-Object { $_.Trim() } | Where-Object { $_ -match '^\d+$' }

    if ($processIds) {
        foreach ($id in $processIds) {
            try {
                Stop-Process -Id $id -Force -ErrorAction Stop
                Write-Host "Process with ID $id terminated." -ForegroundColor Green
            } catch {
                Write-Host "Failed to terminate process with ID $id." -ForegroundColor Red
            }
        }
    } else {
        Write-Host "No valid process IDs entered." -ForegroundColor Red
    }
} else {
    Write-Host "No processes selected for termination." -ForegroundColor Cyan
}

Write-Host "`nPress any key to exit..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
