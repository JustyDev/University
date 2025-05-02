//---------------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;


// �������� ���������� ��������� ��������
bool __fastcall TForm1::IsInputValid()
{
	// ���������, ��� ���� �� ������
	if (LabeledEdit1->Text.Trim() == "" || LabeledEdit2->Text.Trim() == "") {
		return false;
	}

	try {
		// ���������, ��� ������� �����
		int val1 = StrToInt(LabeledEdit1->Text);
		int val2 = StrToInt(LabeledEdit2->Text);
        return true;
	}
	catch (EConvertError &e) {
		// ���� �������� ������ ����������� - ������ ������� �� �����
		return false;
	}
}

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
UpdateButtonsState();
}

// ���������� ��������� ������
void __fastcall TForm1::UpdateButtonsState()
{
    bool isValid = IsInputValid();

    // ��������� ��������� ���� ������ ��������
    Button1->Enabled = isValid;
    Button2->Enabled = isValid;
    Button3->Enabled = isValid;
    Button4->Enabled = isValid;
    Button5->Enabled = isValid;
    Button6->Enabled = isValid;
}

// ���������� ��������� ������ � ������ ���� �����
void __fastcall TForm1::LabeledEdit1Change(TObject *Sender)
{
    UpdateButtonsState();
}

//---------------------------------------------------------------------------
// ���������� ��������� ������ �� ������ ���� �����
void __fastcall TForm1::LabeledEdit2Change(TObject *Sender)
{
    UpdateButtonsState();
}

class MyInt {
	private:
		int I;
	public:
		MyInt() { I=0; }
		MyInt(int i) { I=i; }
		void show(){
			Form1->Memo1->Lines->Add(I);
		}

		// �������� �������� (��� ����)
		MyInt operator+(MyInt a2) {
			return (I + a2.I);
		}

		// �������� ���������
		MyInt operator-(MyInt a2) {
			return (I - a2.I);
		}

		// �������� ���������
        MyInt operator*(MyInt a2) {
            return (I * a2.I);
        }

        // �������� �������
		MyInt operator/(MyInt a2) {
            if (a2.I == 0) {
                Form1->Memo1->Lines->Add("������: ������� �� ����!");
                return 0;
            }
			return (I / a2.I);
        }

		// �������� ��������� < (��� ����)
		bool operator<(MyInt a2) {
			if(I < a2.I) return true;
			else return false;
		}

		// �������� ���������
        bool operator==(MyInt a2) {
            return (I == a2.I);
        }
};

//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	// ��������
	MyInt i1, i2, i3;
	i1 = StrToInt(LabeledEdit1->Text);
	i2 = StrToInt(LabeledEdit2->Text);
	i3 = i1 + i2;
	i3.show();
}

void __fastcall TForm1::Button2Click(TObject *Sender)
{
    // ���������
    MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
	i3 = i1 - i2;
    i3.show();
}

void __fastcall TForm1::Button3Click(TObject *Sender)
{
    // ���������
    MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
    i3 = i1 * i2;
    i3.show();
}

void __fastcall TForm1::Button4Click(TObject *Sender)
{
    // �������
    MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
    i3 = i1 / i2;
    i3.show();
}

void __fastcall TForm1::Button5Click(TObject *Sender)
{
	// ��������� <
	MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
    if(i1 < i2) Form1->Memo1->Lines->Add("������");
    else Form1->Memo1->Lines->Add("����");
}

void __fastcall TForm1::Button6Click(TObject *Sender)
{
	// ��������� ==
	MyInt i1, i2, i3;
	i1 = StrToInt(LabeledEdit1->Text);
	i2 = StrToInt(LabeledEdit2->Text);
	if(i1 == i2) Form1->Memo1->Lines->Add("������");
	else Form1->Memo1->Lines->Add("����");
}

void __fastcall TForm1::Button7Click(TObject *Sender)
{
	Form1->Memo1->Clear();
}
