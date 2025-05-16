# Requesting user input
$folderPath = Read-Host "Enter the folder path"
$extension = Read-Host "Enter the file extension (e.g., txt, jpg, ps1)"
$oldPart = Read-Host "Enter the part of the name you want to replace"
$newPart = Read-Host "Enter the new part of the name"

# Check if the folder exists
if (Test-Path $folderPath) {
    # Search for files with the specified extension
    $files = Get-ChildItem -Path $folderPath -Filter "*.$extension" -File

    if ($files.Count -eq 0) {
        Write-Host "No files with the extension '$extension' were found."
    }
    else {
        foreach ($file in $files) {
            # Check if the file name contains the old part
            if ($file.Name -match $oldPart) {
                $newName = $file.Name -replace $oldPart, $newPart
                $newPath = Join-Path -Path $folderPath -ChildPath $newName

                # Rename the file
                Rename-Item -Path $file.FullName -NewName $newName
                Write-Host "File '$($file.Name)' renamed to '$newName'"
            }
        }
    }
}
else {
    Write-Host "The folder '$folderPath' does not exist."
}
