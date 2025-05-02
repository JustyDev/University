//---------------------------------------------------------------------------

#ifndef Unit2H
#define Unit2H
#include <math.h>
#include "Unit1.h"
using namespace std;
//---------------------------------------------------------------------------


/*struct Figura{
    int x1;
    int y1;
    int x2;
    int y2;
    AnsiString Cvet;
    AnsiString TipFigury;
};*/

int RabotaSKoordinatami(Figura *m,int& XX,int& YY,int& k,int& n);
void Peremeshenie(Figura *mas,int& k,int& dX,int& dY,int& FX,int& FY,int& nom);
void RisyemPoUsery(Figura *m, int& Tip, int& k);
void RisyemPoStructure(Figura *m,int& k);


#endif
