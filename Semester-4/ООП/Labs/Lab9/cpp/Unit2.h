#ifndef Unit2_H
#define Unit2_H

const int N = 256;
extern int ProductType;

class Tovar {
protected:
    char name[N];
    int number;
    float price;
public:
	virtual void add_rec();
    virtual void show();
	float get_price();
    virtual ~Tovar() {}
};

class TovarProd : public Tovar {
private:
	int term;
	int temp;
public:
	void add_rec();
	void show();
    ~TovarProd () {};
};

class TovarProm : public Tovar {
	public:
		~TovarProm () {};
};

#endif

