
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
    int carPosition;      // X-������� ������
    int carY;             // Y-������� ������
    bool carMoving;
    int currentPaymentType; // 1 - ��������, 2 - �����������
    int roadY;            // ������� ���������� ������
    int roadHeight;       // ������ ������
    TColor carColor;      // ���� ������

    void AnimateCar(int paymentType);
    void GenerateRandomCar();
	void DrawRoad(TCanvas *Canvas);  // ��������� ������
	void DrawCar(TCanvas *Canvas);   // ��������� ������
public:        // User declarations
    __fastcall TForm1(TComponent* Owner);
};

class PayRoad {  // ����� ������� ������
	private:
        int Cars;
        float Cash;
        float NonCash;
    public:
        PayRoad() { Cars=0; Cash=0.0; NonCash=0.0; }
        void paying(int flag); // ����������� ������� ����������
        void sum(int flag);    // ��������� �������
        void total(PayRoad car1, PayRoad car2);  // ������� ����� �� ���. � ������. ��������
        void show(int flag);   // ������� showmessage
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif

