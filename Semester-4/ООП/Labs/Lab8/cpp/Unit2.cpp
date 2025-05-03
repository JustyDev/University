
//---------------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "Unit2.h"
#include "Unit1.h"  // To access Form1
//---------------------------------------------------------------------------
#pragma package(smart_init)

// Implementation of base class methods
Float::Float() {
	f = 0;
}

Float::Float(float d) {
    f = d;
}

void Float::show(TPanel* panel) {  // Fully qualify TPanel
    panel->Caption = f;
}

Float Float::operator+(Float b) {
	return Float(f + b.f);
}

