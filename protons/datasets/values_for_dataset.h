#include "TApplication.h"
#include "fstream"
#include "iostream"
#include "algorithm"
#include "iterator"


void values_for_dataset(std::vector<Int_t> & v, TString period = "LHC10b", TString datsetspath = "../datasets/")
{
	cout << period << endl;
    std::ifstream file(datsetspath + period + ".txt");
    std::copy(std::istream_iterator<Int_t>(file), std::istream_iterator<Int_t>(),
                                                 std::back_inserter(v));

    std::cout << "Reading: " << v.size() << " values for dataset: " << period  << std::endl;
}