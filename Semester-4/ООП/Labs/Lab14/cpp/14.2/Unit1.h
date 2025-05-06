//---------------------------------------------------------------------------

#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
#include <Vcl.Dialogs.hpp>
#include <Vcl.ExtCtrls.hpp>
#include <Vcl.Grids.hpp>
#include <Vcl.Mask.hpp>
#include <Vcl.WinXPickers.hpp>
#include <Vcl.ComCtrls.hpp>
#include <vector>
#include <algorithm>
#include <queue>


class FlightQueue;

class Reis {
public:
	String name;
	String type;
	int kol;
	float price;
	TDate date;

	Reis(String n, String t, int k, float p, TDate d)
		: name(n), type(t), kol(k), price(p), date(d) {}

	static void SortByName(TStringGrid *grid);
	static void SortByPrice(TStringGrid *grid);
	static void AddToGrid(TStringGrid *grid, const Reis &r);
	static void SaveToFile(TStringGrid *grid, String filename);
	static void LoadFromFile(TStringGrid *grid, String filename, FlightQueue& queue);
};

class FlightQueue {
private:
	std::queue<Reis> flights;
    void FillGridRow(TStringGrid* grid, int row, const Reis& flight) {
        grid->Cells[0][row] = flight.name;
        grid->Cells[1][row] = flight.type;
        grid->Cells[2][row] = IntToStr(flight.kol);
        grid->Cells[3][row] = FloatToStrF(flight.price, ffFixed, 8, 2);
        grid->Cells[4][row] = FormatDateTime("dd.mm.yyyy", flight.date);
    }

public:
    void Enqueue(const Reis& r) {
        flights.push(r);
    }

    Reis Dequeue() {
        Reis flight = flights.front();
        flights.pop();
        return flight;
    }

    bool IsEmpty() const {
        return flights.empty();
    }

    Reis Peek() const {
        return flights.front();
    }

    void ForEach(std::function<void(const Reis&)> action) const {
        std::queue<Reis> temp = flights;
        while (!temp.empty()) {
            action(temp.front());
            temp.pop();
        }
	}

     void DisplayQueue(TStringGrid* grid, bool sortByDate = false) {
		grid->RowCount = 1;

		if (sortByDate) {
            std::vector<Reis> sortedFlights;

            auto temp = flights;
            while (!temp.empty()) {
                sortedFlights.push_back(temp.front());
                temp.pop();
            }

            std::sort(sortedFlights.begin(), sortedFlights.end(),
                [](const Reis& a, const Reis& b) {
                    return a.date < b.date;
                });

            for (size_t i = 0; i < sortedFlights.size(); i++) {
                int row = i + 1;
                grid->RowCount = row + 1;
                FillGridRow(grid, row, sortedFlights[i]);
            }
        } else {
			auto temp = flights;
            int row = 1;
            while (!temp.empty()) {
                grid->RowCount = row + 1;
                FillGridRow(grid, row, temp.front());
                temp.pop();
                row++;
            }
        }
    }
};
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:	// IDE-managed Components
	TStringGrid *StringGrid1;
	TButton *ButtonAdd;
	TButton *ButtonSave;
	TButton *ButtonLoad;
	TButton *ButtonSortByName;
	TButton *ButtonSortByPrice;
	TLabeledEdit *LE_Reis;
	TLabeledEdit *LE_Type;
	TLabeledEdit *LE_Kol;
	TLabeledEdit *LE_Price;
	TOpenDialog *OpenDialog1;
	TSaveDialog *SaveDialog1;
	TButton *ButtonDeparture;
	TDateTimePicker *DateTimePicker1;
	void __fastcall FormCreate(TObject *Sender);
	void __fastcall ButtonAddClick(TObject *Sender);
	void __fastcall ButtonSaveClick(TObject *Sender);
	void __fastcall ButtonLoadClick(TObject *Sender);
	void __fastcall ButtonSortByNameClick(TObject *Sender);
	void __fastcall ButtonSortByPriceClick(TObject *Sender);
	void __fastcall ButtonDepartureClick(TObject *Sender);
private:
	FlightQueue flightQueue;	// User declarations
public:		// User declarations
	__fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
