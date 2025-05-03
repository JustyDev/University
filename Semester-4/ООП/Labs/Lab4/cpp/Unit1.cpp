//---------------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;

PayRoad CarCash, CarNonCash, TotalCars;

void PayRoad::paying(int flag){ // ����������� ������� ����������
  Cars++;
  if(flag==1) Cash+=500.50;
  if(flag==2) NonCash+=500.50;
}

void PayRoad::show(int flag){
   if(flag==1) Form1->LabeledEdit1->Text = Cars;
   if(flag==2) Form1->LabeledEdit2->Text = Cars;
}

void PayRoad::sum(int flag) {
  if(flag==1) ShowMessage(Cash);
  if(flag==2) ShowMessage(NonCash);
}

void PayRoad::total(PayRoad car1, PayRoad car2) {
  Cars = car1.Cars + car2.Cars;
  Cash = car1.Cash + car2.Cash;
  NonCash = car1.NonCash + car2.NonCash;
  AnsiString s = "����� �������� �����: " + IntToStr(Cars) + "." + " ����� �������: " + FloatToStr(Cash+NonCash);
  ShowMessage(s);
}
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
  : TForm(Owner)
{
  carPosition = -100;
  carMoving = false;
  currentPaymentType = 0;
  carColor = clRed;

  // ������������� ��� ������������
  RandomCarTimer->Enabled = false;
  RandomCarTimer->Interval = 2000; // 2 ������� ����� ���������� ��������

  AnimationTimer->Enabled = false;
  AnimationTimer->Interval = 30; // �������� ��� �������� ��������

  // ����������� ������ - ��� ����� � ������ ����� �����
  roadHeight = 80;
  // roadY ����� ��������� � FormCreate
}
//---------------------------------------------------------------------------
void __fastcall TForm1::FormCreate(TObject *Sender)
{
  // ������������ ��������� ������ (����� �����, �� ���� ������)
  roadY = ClientHeight - roadHeight - 100;

  // ��������� ������� ������ �� Y (�� ������ ������)
  carY = roadY + roadHeight/2 - 20; // 20 - �������� ������ ������

  // ������������� DoubleBuffered ��� ���������� �������� ��� ��������
  DoubleBuffered = true;
}
//---------------------------------------------------------------------------
// ��������� ���� �����
void __fastcall TForm1::FormPaint(TObject *Sender)
{
  // ������ ������
  DrawRoad(Canvas);

  // ������ ������, ���� ��� ������
  if (carMoving || carPosition > -100) {
    DrawCar(Canvas);
  }
}
//---------------------------------------------------------------------------
// ������ ������
void TForm1::DrawRoad(TCanvas *Canvas)
{
  // ������ ����� ������
  Canvas->Brush->Color = clGray;
  Canvas->FillRect(TRect(0, roadY, ClientWidth, roadY + roadHeight));

  // ������ ������ �������
  Canvas->Brush->Color = clYellow;
  Canvas->FillRect(TRect(0, roadY, ClientWidth, roadY + 5));
  Canvas->FillRect(TRect(0, roadY + roadHeight - 5, ClientWidth, roadY + roadHeight));

  // ������ ���������� �������� �� ������ ������
  Canvas->Pen->Color = clWhite;
  Canvas->Pen->Width = 3;
  Canvas->Pen->Style = psDot;

  int centerY = roadY + roadHeight/2;
  Canvas->MoveTo(0, centerY);
  Canvas->LineTo(ClientWidth, centerY);

  // ���������� ����� ���� � �������� ��� ��������� ���������
  Canvas->Pen->Style = psSolid;
  Canvas->Pen->Width = 1;
}
//---------------------------------------------------------------------------
// ������ ������
void TForm1::DrawCar(TCanvas *Canvas)
{
  // ������� ������
  int carWidth = 80;
  int carHeight = 40;

  // �������� ����� ������
  Canvas->Brush->Color = carColor;
  Canvas->Pen->Color = clBlack;
  Canvas->Rectangle(carPosition, carY, carPosition + carWidth, carY + carHeight);

  // ������ ������
  Canvas->Rectangle(carPosition + carWidth/3, carY + 5, carPosition + 2*carWidth/3, carY + carHeight - 5);

  // ������
  Canvas->Brush->Color = clBlack;
  Canvas->Ellipse(carPosition + 10, carY + carHeight - 10, carPosition + 25, carY + carHeight + 5);
  Canvas->Ellipse(carPosition + carWidth - 25, carY + carHeight - 10, carPosition + carWidth - 10, carY + carHeight + 5);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button3Click(TObject *Sender)
{
  CarCash.sum(1);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button4Click(TObject *Sender)
{
  CarNonCash.sum(2);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button5Click(TObject *Sender)
{
  TotalCars.total(CarCash, CarNonCash);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::RandomButtonClick(TObject *Sender)
{
  // ��������� ��� ������������� ������ ��������� �����
  RandomCarTimer->Enabled = !RandomCarTimer->Enabled;
  if (RandomCarTimer->Enabled) {
	RandomButton->Caption = "���������� ���������";
    GenerateRandomCar(); // ����� ���������� ������ ������
  } else {
	RandomButton->Caption = "���������� ���������";
  }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::RandomCarTimerTimer(TObject *Sender)
{
  GenerateRandomCar();
}
//---------------------------------------------------------------------------
void TForm1::GenerateRandomCar()
{
  // ���� ��� ���� ��������, �� ��������� �����
  if (carMoving) return;

  // �������� �������� ��� ������ (1 = ��������, 2 = �����������)
  int paymentType = (rand() % 2) + 1;

  // ��������� ������
  AnimateCar(paymentType);
}
//---------------------------------------------------------------------------
void TForm1::AnimateCar(int paymentType)
{
  currentPaymentType = paymentType;

  // ������������� ��������� ������� ������
  carPosition = -100;

  // ������������� ���� ������ � ����������� �� ���� ������
  carColor = (paymentType == 1) ? clGreen : clBlue;

  // ��������� ��������
  carMoving = true;
  AnimationTimer->Enabled = true;

  // ���������� �����������
  Invalidate();
}
//---------------------------------------------------------------------------
void __fastcall TForm1::AnimationTimerTimer(TObject *Sender)
{
  if (carMoving) {
    // ������� ������
    carPosition += 10;

    // �������������� ����� ��� ���������� ������� ������
    Invalidate();

    // ���� ������ �������� ������� ���� �����
    if (carPosition > ClientWidth) {
      // ������������� ��������
      carMoving = false;
      AnimationTimer->Enabled = false;

      // ������������ ������ � ������
      if (currentPaymentType == 1) {
        CarCash.paying(1);
        CarCash.show(1);
      } else if (currentPaymentType == 2) {
        CarNonCash.paying(2);
        CarNonCash.show(2);
      }

      // ���������� ������� ������
      carPosition = -100;

      // �������������� ����� ��� ������� ������
      Invalidate();
    }
  }
}
//---------------------------------------------------------------------------
