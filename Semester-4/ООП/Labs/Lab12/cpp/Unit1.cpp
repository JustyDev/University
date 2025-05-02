#include <fmx.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.fmx"
TForm1 *Form1;
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm3D(Owner)
{
	// ��������� �������� ��� ������
    FAngle = 0;
	FMajorAxis = 12.0;    // ������ ������� ������� (�� X)
	FMinorAxis = 7.0;    // ������ ����� ������� (�� Z)
	FOrbitSpeed = 0.02;  // �������� �������� �� ������
	FSpinSpeed = 1.0;    // �������� �������� ������ ���

    // ��������� �������� ��� ������ ����
	FMoonAngle = 0;
	FMoonDistance = 5;   // ���������� �� ����� �� ����
	FMoonOrbitSpeed = 0.07; // ���� �������� ������� ������ �����
	FMoonSpinSpeed = 0.5;   // ���� ��������� ���������

    // ������� ������
    FOrbitTimer = new TTimer(this);
	FOrbitTimer->Interval = 16;  // �������� 60 FPS
	FOrbitTimer->OnTimer = OrbitTimerEvent;
	FOrbitTimer->Enabled = true;

    // ���������� "������" � ������
    StrokeCube1->Position->X = 0;
	StrokeCube1->Position->Y = 0;
	StrokeCube1->Position->Z = 0;

    // ��������� ��������� "�����" �� ������
	Sphere1->Position->X = FMajorAxis;
    Sphere1->Position->Y = 0;
    Sphere1->Position->Z = 0;

    // ��������� ��������� "����" ������������ "�����"
    MoonSphere->Position->X = Sphere1->Position->X + FMoonDistance;
    MoonSphere->Position->Y = 0;
    MoonSphere->Position->Z = 0;

    // ��������� ������� ���� (������ �����)
    MoonSphere->Width = Sphere1->Width * 0.27;
	MoonSphere->Height = Sphere1->Height * 0.27;
	MoonSphere->Depth = Sphere1->Depth * 0.27;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::StrokeCube1MouseDown(TObject *Sender, TMouseButton Button,
          TShiftState Shift, float X, float Y, TVector3D &RayPos, TVector3D &RayDir)

{
     FDown = ::PointF(X, Y);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::StrokeCube1MouseMove(TObject *Sender, TShiftState Shift, float X,
		  float Y, TVector3D &RayPos, TVector3D &RayDir)
{
	if (Shift.Contains(ssLeft)) {
	  StrokeCube1->RotationAngle->X = StrokeCube1->RotationAngle->X - ((Y - FDown.Y) * 0.3);
      StrokeCube1->RotationAngle->Y = StrokeCube1->RotationAngle->Y + ((X - FDown.X) * 0.3);

	  FDown = ::PointF(X, Y);
   }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Sphere1MouseDown(TObject *Sender, TMouseButton Button, TShiftState Shift,
		  float X, float Y, TVector3D &RayPos, TVector3D &RayDir)
{
	  FDown = ::PointF(X, Y);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Sphere1MouseMove(TObject *Sender, TShiftState Shift, float X,
		  float Y, TVector3D &RayPos, TVector3D &RayDir)
{
	if (Shift.Contains(ssLeft)) {
	  Sphere1->RotationAngle->X = Sphere1->RotationAngle->X - ((Y - FDown.Y) * 0.3);
	  Sphere1->RotationAngle->Y = Sphere1->RotationAngle->Y + ((X - FDown.X) * 0.3);

	  FDown = ::PointF(X, Y);
   }
}
//---------------------------------------------------------------------------

//---------------------------------------------------------------------------
void __fastcall TForm1::Cone1MouseDown(TObject *Sender, TMouseButton Button, TShiftState Shift,
		  float X, float Y, TVector3D &RayPos, TVector3D &RayDir)
{
	  FDown = ::PointF(X, Y);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Cone1MouseMove(TObject *Sender, TShiftState Shift, float X,
		  float Y, TVector3D &RayPos, TVector3D &RayDir)
{

	if (Shift.Contains(ssAlt)) {
    // ����������� �� X � Y
    Cone1->Position->X = Cone1->Position->X + ((X - FDown.X) * 0.05);
	Cone1->Position->Y = Cone1->Position->Y - ((Y - FDown.Y) * 0.05);
  }
  else if (Shift.Contains(ssCtrl)) {
    // ����������� �� Z ��� ������� Ctrl
    Cone1->Position->Z = Cone1->Position->Z + ((X - FDown.X) * 0.05);
  }

	if (Shift.Contains(ssLeft)) {
	  Cone1->RotationAngle->X = Cone1->RotationAngle->X - ((Y - FDown.Y) * 0.3);
	  Cone1->RotationAngle->Y = Cone1->RotationAngle->Y + ((X - FDown.X) * 0.3);
   }

   FDown = ::PointF(X, Y);
}
//---------------------------------------------------------------------------

void __fastcall TForm1::OrbitTimerEvent(TObject *Sender)
{
    // ����������� ����
    FAngle += FOrbitSpeed;
    if (FAngle > 6.28318) // 2*Pi
        FAngle -= 6.28318;

    // ��������� ��������� �� �������
    float x = FMajorAxis * cos(FAngle);
    float z = FMinorAxis * sin(FAngle);

    // ��������� ��������� "�����"
    Sphere1->Position->X = x;
    Sphere1->Position->Z = z;

    // ������� "�����" ������ ����������� ��� Y
    Sphere1->RotationAngle->Y += FSpinSpeed;
    if (Sphere1->RotationAngle->Y > 360)
		Sphere1->RotationAngle->Y -= 360;

    // ����������� ���� ����
    FMoonAngle += FMoonOrbitSpeed;
    if (FMoonAngle > 6.28318)
        FMoonAngle -= 6.28318;

    // ��������� ��������� ���� ������������ �����
    float moonRelativeX = FMoonDistance * cos(FMoonAngle);
    float moonRelativeZ = FMoonDistance * sin(FMoonAngle);

	// ��������� ��������� "����" (��������� � ����������� �����)
    MoonSphere->Position->X = Sphere1->Position->X + moonRelativeX;
    MoonSphere->Position->Z = Sphere1->Position->Z + moonRelativeZ;
    MoonSphere->Position->Y = Sphere1->Position->Y; // �� �� ������, ��� � � �����

    // ������� "����" ������ ����������� ��� Y
	MoonSphere->RotationAngle->Y += FMoonSpinSpeed;
    if (MoonSphere->RotationAngle->Y > 360)
		MoonSphere->RotationAngle->Y -= 360;

}

void __fastcall TForm1::TrackBarMoonSpeedChange(TObject *Sender)
{
	FMoonOrbitSpeed = TrackBarMoonSpeed->Value / 1000.0;
}


