//---------------------------------------------------------------------------

#pragma hdrstop
#include <math.h>

#include "Unit2.h"
#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)

using namespace std;

//функция для определения является ли координата частью фигуры
int RabotaSKoordinatami(Figura *m,int& XX,int& YY,int& k,int& n){
    for (int j=0; j < k; j++) {
        /*int xCentr=(m[j].x1+m[j].x2)/2;
        int yCentr=(m[j].y1+m[j].y2)/2;
        int a=abs(m[j].x2-xCentr);
        int b=abs(m[j].y2-yCentr); */
        int x1, x2, y1, y2;
        if (m[j].x1>m[j].x2) {
            x1=m[j].x2;
            x2=m[j].x1;
        }
        else{
            x1=m[j].x1;
            x2=m[j].x2;
        }
        if (m[j].y1>m[j].y2) {
            y1=m[j].y2;
            y2=m[j].y1;
        }
        else{
            y1=m[j].y1;
            y2=m[j].y2;
        }
        if (m[j].TipFigury=="Line"){

            for(int x=XX-5; x<XX+5; x++){
                for(int y=YY-5; y<YY+5; y++){
                    if((y/x==m[j].y1/m[j].x1)
                    &&(y>=y1)&&(y<=y2)&&(x>=x1)
                    &&(x<=x2)){
                        n=j;
                        return 1;
                    } //?
                }
                //if(flag3==1) break;
            }
        }
        if ((m[j].TipFigury=="Rectangle")&&
        (((abs(XX-x1)<=5||abs(XX-x2)<=5)&&(YY>=y1-5)&&(YY<=y2+5))||
        ((abs(YY-y1)<=5||abs(YY-y2)<=5)&&(XX>=x1-5)&&(XX<=x2+5)))){
            n=j;
            return 1;
        }
        if (m[j].TipFigury=="Ellipse"){
            /*for(int x=X-10; x<X+10; a++){
            for(int y=Y-10; y<Y+10; b++){
            if (((((x-xCentr)^2)/(a^2))+(((y-yCentr)^2)/(b^2)))==1){
            flag3=1; //?
            break;
            }
            }
            if (flag3==1) break;

            }*/
            if(((abs(XX-x1)<=5||abs(XX-x2)<=5)&&(YY>=y1-5)&&(YY<=y2+5))||
            ((abs(YY-y1)<=5||abs(YY-y2)<=5)&&(XX>=x1-5)&&(XX<=x2+5))){
                n=j;
                return 1;
            }
        }
    }
    return 0;
}

void Peremeshenie(Figura *mas,int& k,int& dX,int& dY,int& FX,int& FY,int& nom){
    //стираем
    Form1->Image1->Canvas->Pen->Color=clWhite;
    Form1->Image1->Canvas->Brush->Color=clWhite;
    RisyemPoStructure(mas, nom);

    mas[nom].x1+=dX;
    mas[nom].x2+=dX;
    mas[nom].y1+=dY;
    mas[nom].y2+=dY;

    FX+=dX;
    FY+=dY;

    //рисуем
    Form1->Image1->Canvas->Pen->Color=StringToColor(mas[nom].Cvet);
    Form1->Image1->Canvas->Brush->Style=bsClear;
    RisyemPoStructure(mas, nom);

    //рисуем все фигуры
    for (int j=0; j < k; j++) {
        Form1->Image1->Canvas->Pen->Color=StringToColor(mas[j].Cvet);
        Form1->Image1->Canvas->Brush->Style=bsClear;
        RisyemPoStructure(mas, j);
    }
}

void RisyemPoUsery(Figura *m, int& Tip, int& k){
        if (Tip==0) {
            m[k].TipFigury="Line";
            Form1->Image1->Canvas->MoveTo(m[k].x1,m[k].y1);
            Form1->Image1->Canvas->LineTo(m[k].x2,m[k].y2);
        }
        if (Tip==1) {
            m[k].TipFigury="Rectangle";
            Form1->Image1->Canvas->Rectangle(m[k].x1,m[k].y1,
                                        m[k].x2,m[k].y2);
        }
        if (Tip==2) {
            m[k].TipFigury="Ellipse";
            Form1->Image1->Canvas->Ellipse(m[k].x1,m[k].y1,
                                        m[k].x2,m[k].y2);
        }
}

//функция для рисования если фигура уже есть
void RisyemPoStructure(Figura *m,int& k){
            if (m[k].TipFigury=="Line") {
                Form1->Image1->Canvas->MoveTo(m[k].x1,m[k].y1);
                Form1->Image1->Canvas->LineTo(m[k].x2,m[k].y2);
            }
            if (m[k].TipFigury=="Rectangle") {
                Form1->Image1->Canvas->Rectangle(m[k].x1,m[k].y1,
                                            m[k].x2,m[k].y2);
            }
            if (m[k].TipFigury=="Ellipse") {
                Form1->Image1->Canvas->Ellipse(m[k].x1,m[k].y1,
                                            m[k].x2,m[k].y2);
            }
}
