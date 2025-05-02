//---------------------------------------------------------------------------

#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <FMX.Controls.hpp>
#include <FMX.Forms.hpp>
#include <FMX.Forms3D.hpp>
#include <FMX.Ani.hpp>
#include <FMX.Controls3D.hpp>
#include <FMX.MaterialSources.hpp>
#include <FMX.Objects3D.hpp>
#include <FMX.Types.hpp>
#include <System.Math.Vectors.hpp>
#include <FMX.Controls.Presentation.hpp>
#include <FMX.StdCtrls.hpp>
//--------------------------------------------------------------------------
class TForm1 : public TForm3D
{
__published:    // IDE-managed Components
	TSphere *Sphere1;
    TTextureMaterialSource *TextureMaterialSource1;
    TFloatAnimation *FloatAnimation1;
	TStrokeCube *StrokeCube1;
    TFloatAnimation *FloatAnimation2;
	TSphere *MoonSphere;
	TTextureMaterialSource *MoonMaterial;
	TTrackBar *TrackBarMoonSpeed;
	TCone *Cone1;
	TTextureMaterialSource *PyramidMaterial;
	void __fastcall StrokeCube1MouseDown(TObject *Sender, TMouseButton Button, TShiftState Shift,
        float X, float Y, TVector3D &RayPos, TVector3D &RayDir);
	void __fastcall StrokeCube1MouseMove(TObject *Sender, TShiftState Shift, float X,
        float Y, TVector3D &RayPos, TVector3D &RayDir);
	void __fastcall Sphere1MouseDown(TObject *Sender, TMouseButton Button, TShiftState Shift,
		float X, float Y, TVector3D &RayPos, TVector3D &RayDir);
	void __fastcall Sphere1MouseMove(TObject *Sender, TShiftState Shift, float X, float Y,
		TVector3D &RayPos, TVector3D &RayDir);
	void __fastcall TrackBarMoonSpeedChange(TObject *Sender);


	void __fastcall Cone1MouseDown(TObject *Sender, TMouseButton Button, TShiftState Shift,
		float X, float Y, TVector3D &RayPos, TVector3D &RayDir);
	void __fastcall Cone1MouseMove(TObject *Sender, TShiftState Shift, float X, float Y,
		TVector3D &RayPos, TVector3D &RayDir);
private:    // User declarations
	TPointF FDown;

    float FAngle;
	float FMajorAxis;
	float FMinorAxis;
	float FOrbitSpeed;
	float FSpinSpeed;
	TTimer* FOrbitTimer;

    float FMoonAngle;      // Угол Луны вокруг Земли
	float FMoonDistance;   // Расстояние от Земли до Луны
	float FMoonOrbitSpeed; // Скорость движения Луны вокруг Земли
	float FMoonSpinSpeed;  // Скорость вращения Луны

	void __fastcall OrbitTimerEvent(TObject *Sender);
public:     // User declarations
	__fastcall TForm1(TComponent* Owner);
};
//--------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//--------------------------------------------------------------------------
#endif
