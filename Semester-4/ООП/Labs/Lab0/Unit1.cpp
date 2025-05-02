//---------------------------------------------------------------------------

#include <vcl.h>
#include <fstream>
#include <math.h>
#pragma hdrstop

#include "Unit1.h"
#include "Unit2.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
using namespace std;
TForm1 *Form1;
//линия странно захватывается, не отработаны значения загружаемые
int i=0;//счетчик точек
const int KF=1000;
Figura  massiv_figur[KF];
int ColorFromUser;
int TipFromUser;
int flag1=0, flag2=0;//рисование-передвижение
int nomer, deltaX, deltaY, FirstX, FirstY, tip;

int KolFigur=0;
Figura *mf;




//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
    : TForm(Owner)
{
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Image1MouseDown(TObject *Sender, TMouseButton Button, TShiftState Shift,
          int X, int Y)
{
    if (Shift.Contains(ssLeft)){
        flag2=0;
            if(i>0){
                if (RabotaSKoordinatami(massiv_figur, X, Y, i, nomer)==1){

                    FirstX=X;
                    FirstY=Y;
                    tip=1;
                    flag2=1;


                }
            }

            if(KolFigur>0&&flag2==0){
                if (RabotaSKoordinatami(mf, X, Y, KolFigur, nomer)==1){

                    FirstX=X;
                    FirstY=Y;
                    tip=2;
                    flag2=1;


                }
            }
            //break;
        //}

        if (flag2==0) {
            massiv_figur[i].x1=X;
            massiv_figur[i].y1=Y;
            ColorFromUser=RadioGroup1->ItemIndex;
            if (ColorFromUser==0) massiv_figur[i].Cvet="clRed";
            if (ColorFromUser==1) massiv_figur[i].Cvet="clGreen";
            if (ColorFromUser==2) massiv_figur[i].Cvet="clBlue";

            Image1->Canvas->Pen->Color=StringToColor(massiv_figur[i].Cvet);

            TipFromUser=RadioGroup2->ItemIndex;
            flag1=1;
        }

    }
}
//---------------------------------------------------------------------------

void __fastcall TForm1::Image1MouseMove(TObject *Sender, TShiftState Shift, int X,
          int Y)
{
    StatusBar1->SimpleText="X="+IntToStr(X)+"      Y="+IntToStr(Y);
    //int x2Old, y2Old;
    if (flag1==1) {
        //x2Old=massiv_figur[i].x2;
        //y2Old=massiv_figur[i].y2;


        //стираем
        Image1->Canvas->Pen->Color=clWhite;
        Image1->Canvas->Brush->Color=clWhite;
        RisyemPoUsery(massiv_figur, TipFromUser, i);



        massiv_figur[i].x2=X;
        massiv_figur[i].y2=Y;
        //рисуем
        Image1->Canvas->Pen->Color=StringToColor(massiv_figur[i].Cvet);
        Image1->Canvas->Brush->Style=bsClear;
        RisyemPoUsery(massiv_figur, TipFromUser, i);

        //рисуем все фигуры
        for (int j=0; j < i; j++) {
            Image1->Canvas->Pen->Color=StringToColor(massiv_figur[j].Cvet);
            Image1->Canvas->Brush->Style=bsClear;
            RisyemPoStructure(massiv_figur, j);
        }



    }

    if (flag2==1) {
        if (tip==1) {
            deltaX=X-FirstX;
            deltaY=Y-FirstY;
            Peremeshenie(massiv_figur, i, deltaX, deltaY, FirstX, FirstY, nomer);
        }

        if (tip==2) {
            deltaX=X-FirstX;
            deltaY=Y-FirstY;

            Peremeshenie(mf, KolFigur, deltaX, deltaY, FirstX, FirstY, nomer);
        }
    }

}
//---------------------------------------------------------------------------

void __fastcall TForm1::FormCreate(TObject *Sender)
{
    Image1->Canvas->Brush->Color=clWhite;
    Image1->Canvas->FillRect(Rect(0,0, Image1->Width, Image1->Height ));
}
//---------------------------------------------------------------------------

void __fastcall TForm1::Button1Click(TObject *Sender)
{
    if(SaveDialog1->Execute()){
        ofstream fout(SaveDialog1->FileName.w_str());
        if (!fout) {
            Application->MessageBoxW(L"Файловая ошибка ", L"Ошибка ", MB_OK);
            return;
        }
        for(int j=0;j<i;j++){
            fout<<massiv_figur[j].x1<<" "<<massiv_figur[j].y1<<" "
                <<massiv_figur[j].x2<<" "<<massiv_figur[j].y2<<" "
                <<massiv_figur[j].Cvet.c_str()<<" "<<massiv_figur[j].TipFigury.c_str()<<endl;
        }
        fout.close();

        Application->MessageBoxW(SaveDialog1->FileName.w_str(), L"Данные записаны ", MB_OK);

    }
}
//---------------------------------------------------------------------------

void __fastcall TForm1::Button2Click(TObject *Sender)
{
    Image1->Canvas->Brush->Color=clWhite;
    Image1->Canvas->FillRect(Rect(0,0, Image1->Width, Image1->Height ));
    for(int j=0; j<i-1; j++){
            massiv_figur[j].x1=0;
            massiv_figur[j].y1=0;
            massiv_figur[j].x2=0;
            massiv_figur[j].y2=0;
            massiv_figur[j].Cvet="";
            massiv_figur[j].TipFigury="";
    }

    i=0;
}
//---------------------------------------------------------------------------

void __fastcall TForm1::Button3Click(TObject *Sender)
{
	if(OpenDialog1->Execute()){
        ifstream fin(OpenDialog1->FileName.w_str());
        int KolStrok=0;
        char s, cvet[256], t_f[36];
        while (!fin.eof()){
            fin.get(s);
            if (s=='\n') KolStrok++;

        }
        fin.close();
        ifstream fin2(OpenDialog1->FileName.w_str());
        KolFigur=KolStrok-1;

        mf =new Figura[KolFigur];
        for (int j=0; j < KolFigur; j++) {
            fin2 >>mf[j].x1>>mf[j].y1>>
                mf[j].x2>>mf[j].y2>>
                cvet>>t_f;
            mf[j].Cvet=AnsiString(cvet);
            mf[j].TipFigury=AnsiString(t_f);

            Image1->Canvas->Pen->Color=StringToColor(mf[j].Cvet);
            Image1->Canvas->Brush->Style=bsClear;
            RisyemPoStructure(mf, j);
        }
        fin2.close();
    }
}
//---------------------------------------------------------------------------

void __fastcall TForm1::Image1MouseUp(TObject *Sender, TMouseButton Button, TShiftState Shift,
          int X, int Y)
{
    if (flag1==1){
        flag1=0;
        i++;
    }
    if (flag2==1){
        flag2=0;
    }
}
//---------------------------------------------------------------------------
