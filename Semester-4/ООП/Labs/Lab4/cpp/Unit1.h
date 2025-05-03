
//---------------------------------------------------------------------------
#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
#include <Vcl.ExtCtrls.hpp>
#include <Vcl.Mask.hpp>
#include <Vcl.Graphics.hpp>
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:    // IDE-managed Components
    TGroupBox *GroupBox1;
    TLabeledEdit *LabeledEdit1;
    TGroupBox *GroupBox2;
    TLabeledEdit *LabeledEdit2;
    TButton *Button3;
    TButton *Button4;
    TButton *Button5;
    TTimer *AnimationTimer;
    TTimer *RandomCarTimer;
    TButton *RandomButton;
    void __fastcall Button3Click(TObject *Sender);
    void __fastcall Button4Click(TObject *Sender);
    void __fastcall Button5Click(TObject *Sender);
    void __fastcall AnimationTimerTimer(TObject *Sender);
    void __fastcall RandomButtonClick(TObject *Sender);
    void __fastcall RandomCarTimerTimer(TObject *Sender);
    void __fastcall FormCreate(TObject *Sender);
    void __fastcall FormPaint(TObject *Sender);
private:    // User declarations
    int carPosition;      // X-позиция машины
    int carY;             // Y-позиция машины
    bool carMoving;
    int currentPaymentType; // 1 - наличные, 2 - безналичные
    int roadY;            // Верхняя координата дороги
    int roadHeight;       // Высота дороги
    TColor carColor;      // Цвет машины

    void AnimateCar(int paymentType);
    void GenerateRandomCar();
	void DrawRoad(TCanvas *Canvas);  // Рисование дороги
	void DrawCar(TCanvas *Canvas);   // Рисование машины
public:        // User declarations
    __fastcall TForm1(TComponent* Owner);
};

class PayRoad {  // класс платной дороги
	private:
        int Cars;
        float Cash;
        float NonCash;
    public:
        PayRoad() { Cars=0; Cash=0.0; NonCash=0.0; }
        void paying(int flag); // увеличиваем счетчик проехавших
        void sum(int flag);    // суммируем платежи
        void total(PayRoad car1, PayRoad car2);  // считаем итого по нал. и безнал. платежам
        void show(int flag);   // выводим showmessage
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif

