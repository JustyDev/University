if ($args.Count -eq 0) {
    Write-Host "Please provide the folder name as an argument."
    Write-Host "Usage: .\CreateFolder.ps1 <FolderName> [<Path>]"
    exit
}

$newFolderName = $args[0]

if ($args.Count -eq 2) {
    $folderPath = $args[1]
} else {
    $folderPath = Get-Location
}

# Формируем полный путь к новой папке
$newFolderPath = Join-Path -Path $folderPath -ChildPath $newFolderName

if (Test-Path $newFolderPath) {
    Write-Host "The folder '$newFolderPath' already exists."
}
else {
    New-Item -ItemType Directory -Path $newFolderPath | Out-Null
    Write-Host "Folder created: $newFolderName"
}
