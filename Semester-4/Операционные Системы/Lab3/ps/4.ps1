$folderPath = Read-Host "Enter the folder path"
$fileName = Read-Host "Enter the file name or part of it (e.g., report.txt or log)"

# Check if the folder exists
if (Test-Path $folderPath) {
    # Search for the file (including subfolders)
    $files = Get-ChildItem -Path $folderPath -Recurse -File | Where-Object { $_.Name -like "*$fileName*" }

    if ($files) {
        Write-Host "`nFound files:"
        foreach ($file in $files) {
            Write-Host "$($file.Name)"
        }
    }
    else {
        Write-Host "No files matching '$fileName' were found in '$folderPath'."
    }
}
else {
    Write-Host "The folder '$folderPath' does not exist."
}
