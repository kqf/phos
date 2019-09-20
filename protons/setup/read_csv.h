#ifndef READ_CSV_H
#define READ_CSV_H

#include "TApplication.h"
#include "fstream"
#include "iostream"
#include "algorithm"
#include "iterator"
using std::cout;
using std::endl;


void read_csv(std::vector<Int_t> & v, TString period = "LHC10b", TString datsetspath = "../../datasets/")
{
	cout << datsetspath + period << endl;
	std::ifstream file(datsetspath + period + ".txt");
	std::copy(
		std::istream_iterator<Int_t>(file),
		std::istream_iterator<Int_t>(),
		std::back_inserter(v)
	);
	std::cout << "Reading: " << v.size() << " values for dataset: " << period  << std::endl;
}

#endif
