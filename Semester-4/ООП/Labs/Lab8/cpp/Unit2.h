
//---------------------------------------------------------------------------
#ifndef Unit2H
#define Unit2H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.ExtCtrls.hpp>  // Contains TPanel definition

// Base class
class Float {
  protected:
	 float f;
  public:
     Float();
     Float(float d);
	 void show(TPanel* panel);  // Fully qualify TPanel
	 Float operator+(Float b);
};
//---------------------------------------------------------------------------
#endif

