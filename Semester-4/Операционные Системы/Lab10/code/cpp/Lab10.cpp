#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

using namespace std;
namespace fs = filesystem;

void printFileContent(const string&);
void copyFile(const string&, const string&);
void getFileSize(const string&);
void createDirectory(const string&);
void removeDirectory(const string&);
void removeFile(const string&);
void renameFile(const string&, const string&);

int main() {
    unsigned short choice;
    string file1, file2;

    do {
        cout << "\nSelect an action:\n";
        cout << "1. Show file content\n";
        cout << "2. Copy file\n";
        cout << "3. Get file size\n";
        cout << "4. Create directory\n";
        cout << "5. Remove directory\n";
        cout << "6. Delete file\n";
        cout << "7. Rename file\n";
        cout << "0. Exit\n";
        cout << "Your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter file name: ";
                cin >> file1;
                printFileContent(file1);
                break;
            case 2:
                cout << "Enter source file name: ";
                cin >> file1;
                cout << "Enter destination file name: ";
                cin >> file2;
                copyFile(file1, file2);
                break;
            case 3:
                cout << "Enter file name: ";
                cin >> file1;
                getFileSize(file1);
                break;
            case 4:
                cout << "Enter directory name to create: ";
                cin >> file1;
                createDirectory(file1);
                break;
            case 5:
                cout << "Enter directory name to remove: ";
                cin >> file1;
                removeDirectory(file1);
                break;
            case 6:
                cout << "Enter file name to delete: ";
                cin >> file1;
                removeFile(file1);
                break;
            case 7:
                cout << "Enter current file name: ";
                cin >> file1;
                cout << "Enter new file name: ";
                cin >> file2;
                renameFile(file1, file2);
                break;
            case 0:
                break;
            default:
                cout << "Invalid choice. Please try again." << endl;
        }

    } while (choice != 0);

    system("pause");
    return 0;
}


// Print file content
void printFileContent(const string& fileName) {
    ifstream file(fileName);
    if (!file) {
        cerr << "Failed to open file: " << fileName << endl;
        return;
    }

    string line;
    cout << "Content of file \"" << fileName << "\":" << endl;
    while (getline(file, line)) {
        cout << line << endl;
    }

    file.close();
}

// Copy file content to another file
void copyFile(const string& source, const string& destination) {
    ifstream src(source, ios::binary);
    ofstream dest(destination, ios::binary);

    if (!src || !dest) {
        cerr << "Error opening files." << endl;
        return;
    }

    dest << src.rdbuf();

    cout << "File successfully copied from \"" << source << "\" to \"" << destination << "\"" << endl;

    src.close();
    dest.close();
}

// Determine file size
void getFileSize(const string& fileName) {
    if (!fs::exists(fileName)) {
        cerr << "File does not exist: " << fileName << endl;
        return;
    }

    auto size = fs::file_size(fileName);
    cout << "Size of file \"" << fileName << "\": " << size << " bytes" << endl;
}

// Create directory
void createDirectory(const string& dirName) {
    if (fs::exists(dirName)) {
        cerr << "Directory \"" << dirName << "\" already exists." << endl;
        return;
    }

    try {
        if (fs::create_directory(dirName)) {
            cout << "Directory \"" << dirName << "\" successfully created." << endl;
        } else {
            cerr <<"Failed to create directory \"" << dirName << "\"." << endl;
        }
    } catch (const fs::filesystem_error& e) {
        cerr << "Error creating directory: " << e.what() << endl;
    }
}

// Remove directory
void removeDirectory(const string& dirName) {
    if (!fs::exists(dirName)) {
        cerr << "Directory \"" << dirName << "\" does not exist." << endl;
        return;
    }

    if (!fs::is_directory(dirName)) {
        cerr << "\"" << dirName << "\" is not a directory." << endl;
        return;
    }

    try {
        uintmax_t removedCount = fs::remove_all(dirName);
        cout << "Directory \"" << dirName << "\" successfully removed with " << removedCount << " elements." << endl;
    } catch (const fs::filesystem_error& e) {
        cerr << "Error removing directory: " << e.what() << endl;
    }
}

// Delete file
void removeFile(const string& fileName) {
    if (!fs::exists(fileName)) {
        cerr << "File \"" << fileName << "\" does not exist." << endl;
        return;
    }

    if (fs::is_directory(fileName)) {
        cerr << "\"" << fileName << "\" is a directory, not a file." << endl;
        return;
    }

    try {
        if (fs::remove(fileName)) {
            cout << "File \"" << fileName << "\" successfully deleted." << endl;
        } else {
            cerr << "Failed to delete file \"" << fileName << "\"." << endl;
        }
    } catch (const fs::filesystem_error& e) {
        cerr << "Error deleting file: " << e.what() << endl;
    }
}

// Rename file
void renameFile(const string& oldName, const string& newName) {
    if (!fs::exists(oldName)) {
        cerr << "File \"" << oldName << "\" does not exist." << endl;
        return;
    }

    if (fs::exists(newName)) {
        cerr << "File with name \"" << newName << "\" already exists." << endl;
        return;
    }

    try {
        fs::rename(oldName, newName);
        cout << "File \"" << oldName << "\" successfully renamed to \"" << newName << "\"." << endl;
    } catch (const fs::filesystem_error& e) {
        cerr << "Error renaming file: " << e.what() << endl;
    }
}