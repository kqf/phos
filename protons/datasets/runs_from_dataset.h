#include "TApplication.h"
#include "fstream"
#include "iostream"
#include "algorithm"
#include "iterator"


void runs_from_dataset(std::vector<int> & v, TString period = "LHC10b", TString datsetspath = "../datasets/")
{
	cout << period << endl;
    std::ifstream file(datsetspath + period + ".txt");
    std::copy(std::istream_iterator<int>(file), std::istream_iterator<int>(),
                                                 std::back_inserter(v));

    std::cout << "Reading: " << v.size() << " runs." << std::endl;
}