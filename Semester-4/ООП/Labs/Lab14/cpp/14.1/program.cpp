#include <fstream>
#include <iostream>
#include <string>

using namespace std;

struct StackNode {
    string data;
    StackNode* next;
};

class TextStack {
private:
    StackNode* top;
    
public:
    TextStack() : top(nullptr) {}
    
    bool isEmpty() {
        return top == nullptr;
    }
    
    void push(const string& line) {
        StackNode* newNode = new StackNode;
        newNode->data = line;
        newNode->next = top;
        top = newNode;
    }
    
    string pop() {
        if (isEmpty()) {
            return ""; 
        }
        
        StackNode* temp = top;
        string popped = top->data;
        top = top->next;
        delete temp;
        return popped;
    }
    
    string peek() {
        if (isEmpty()) {
            return "";
        }
        return top->data;
    }
    
    ~TextStack() {
        while (!isEmpty()) {
            pop();
        }
    }
};

int main() {
    TextStack fileStack;
    string filename;
    
    cout << "Введите имя файла для чтения: ";
    cin >> filename;
    
    ifstream inputFile(filename);
    
    if (!inputFile.is_open()) {
        cerr << "Ошибка открытия файла!" << endl;
        return 1;
    }
    
    string line;
    
    while (getline(inputFile, line)) {
        fileStack.push(line);
    }
    
    inputFile.close();
    
    cout << "\nСодержимое файла (в обратном порядке):\n";
    while (!fileStack.isEmpty()) {
        cout << fileStack.pop() << endl;
    }
    
    return 0;
}