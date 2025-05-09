
#include <iostream>
#include <windows.h>
#include <direct.h>
#include <io.h>

using namespace std;

bool FileExists(const char*);
bool DirectoryExists(const char*);
void CreateDir(const char*);
void RemoveDir(const char*);
void DeleteFileCustom(const char*);
void RenameFile(const char*, const char*) ;

int main() {
    int choice;
    char name1[260], name2[260];

    do {
        cout << "\nMenu:\n";
        cout << "1. Create folder\n";
        cout << "2. Delete folder\n";
        cout << "3. Delete file\n";
        cout << "4. Rename file\n";
        cout << "0. Exit\n";
        cout << "Select action: ";
        cin >> choice;
        cin.ignore();

        switch (choice) {
            case 1:
                cout << "Enter folder name: ";
                cin.getline(name1, 260);
                CreateDir(name1);
                break;
            case 2:
                cout << "Enter folder name: ";
                cin.getline(name1, 260);
                RemoveDir(name1);
                break;
            case 3:
                cout << "Enter file name: ";
                cin.getline(name1, 260);
                DeleteFileCustom(name1);
                break;
            case 4:
                cout << "Enter current file name: ";
                cin.getline(name1, 260);
                cout << "Enter new file name: ";
                cin.getline(name2, 260);
                RenameFile(name1, name2);
                break;
            case 0:
                cout << "Exit.\n";
                break;
            default:
                cout << "Incorrect choice. Try again.\n";
        }
    } while (choice != 0);

    return 0;
}

bool FileExists(const char* filename) {
    return (_access(filename, 0) != -1 && !(GetFileAttributesA(filename) & FILE_ATTRIBUTE_DIRECTORY));
}

bool DirectoryExists(const char* dirname) {
    DWORD attr = GetFileAttributesA(dirname);
    return (attr != INVALID_FILE_ATTRIBUTES && (attr & FILE_ATTRIBUTE_DIRECTORY));
}

void CreateDir(const char* dirname) {
    if (DirectoryExists(dirname)) {
        cout << "Folder already exists.\n";
    } else {
        if (_mkdir(dirname) == 0) {
            cout << "Folder created successfully.\n";
        } else {
            perror("Error creating folder");
        }
    }
}

void RemoveDir(const char* dirname) {
    if (DirectoryExists(dirname)) {
        if (_rmdir(dirname) == 0) {
            cout << "Folder deleted successfully.\n";
        } else {
            perror("Error deleting folder (possibly not empty)");
        }
    } else {
        cout << "Folder does not exist.\n";
    }
}

void DeleteFileCustom(const char* filename) {
    if (FileExists(filename)) {
        if (remove(filename) == 0) {
            cout << "File deleted successfully.\n";
        } else {
            perror("Error deleting file");
        }
    } else {
        cout << "File does not exist.\n";
    }
}

void RenameFile(const char* oldName, const char* newName) {
    if (FileExists(oldName)) {
        if (rename(oldName, newName) == 0) {
            cout << "File renamed successfully.\n";
        } else {
            perror("Error renaming file");
        }
    } else {
        cout << "File to rename does not exist.\n";
    }
}
