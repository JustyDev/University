/*
  Test file for Python analyzer: tokens break, <<, >>
  The following should be ignored because they are in comments:
  break << >>
*/

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <map>

using namespace std;

struct My {
    int x{};
};

ostream& operator<<(ostream& os, const My& m) {
    os << "My{x=" << m.x << "}";  // contains << (3 times in this line)
    return os;
}

istream& operator>>(istream& is, My& m) {
    is >> m.x;  // contains >>
    return is;
}

int main() {
    // Single-line comment with tokens: break << >> (should be ignored)
    cout << "Start" << endl; // two << occurrences here

    int a = 1, b = 8, c = 0, d = 0;
    c = a << 2;        // <<
    d = b >> 1;        // >>
    c <<= 1;           // should be ignored (<<=)
    d >>= 1;           // should be ignored (>>=)

    // Number with digit separators - not a char literal:
    long big = 1'000'000;
    cout << "big=" << big << "\n"; // three <<

    // Strings containing tokens should be ignored by the analyzer:
    string s1 = "string with break and << and >> inside";
    auto   s2 = u8"юникод со строкой << >> break";
    string raw1 = R"(raw text: << >> break and /* not a comment */)";
    auto   raw2 = u8R"delim(raw with custom delim << >> break and "quotes")delim";

    // Template close '>>' should still be counted by the analyzer as a token sequence:
    vector<vector<int>> vv = {{1,2}, {3,4}};
    map<int, vector<string>> mp;

    // Character literals:
    char ch1 = '>';
    char ch2 = '<';
    char ch3 = '\'';
    char nl  = '\n';

    // Extraction and insertion
    My m{};
    istringstream iss("42");
    iss >> m;          // >>
    cout << m << '\n'; // two <<

    // Breaks in control flow:
    for (int i = 0; i < 10; ++i) {
        if (i == 3) {
            break;    // break #1
        }
        cout << i << ' '; // two <<
    }

    cout << "\n"; // <<

    int x = 0;
    while (true) {
        ++x;
        if (x > 2) break; // break #2 on same line as code
        if (x == 1) {
            // the word break in comment should be ignored: break
            continue;
        }
        cout << x << '\n'; // <<
    }

    int sw = 1;
    switch (sw) {
        case 0:
            cout << "zero\n"; // <<
            break;            // break #3
        case 1:
            cout << "one\n";  // <<
            break;            // break #4
        default:
            cout << "other\n"; // <<
            break;             // break #5
    }

    // Identifiers containing 'break' must not be counted:
    int breakfast = 0;
    int my_break = 123; // not a standalone 'break'

    cout << "End" << endl; // two <<

    return 0;
}
