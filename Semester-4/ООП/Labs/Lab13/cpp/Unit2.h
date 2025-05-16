#ifndef Unit2H
#define Unit2H

class train {
	private:
		String date;
		String time;
		String stop_point;
		int free_space;
	public:
		train() : date(""), time(""), stop_point(""), free_space(0) {};
		virtual ~train() {};
		train(String date, String time, String stop_point, int free_space);

		void set_train(String date, String time, String stop_point, int free_space);

		String get_date() const;
		String get_time() const;
		String get_point() const;
		int get_space() const;
};

train::train(String date, String time, String stop_point, int free_space) {
    this->date = date;
	this->time = time;
	this->stop_point = stop_point;
	this->free_space = free_space;
}

void train::set_train(String date, String time, String stop_point, int free_space) {
	this->date = date;
	this->time = time;
	this->stop_point = stop_point;
	this->free_space = free_space;
}

String train::get_date() const{
	return this->date;
}

String train::get_time() const {
	return this->time;
}

String train::get_point() const {
	return this->stop_point;
}

int train::get_space() const {
	return this->free_space;
}

#endif