#include "TApplication.h"
#include "fstream"
#include "iostream"
#include "algorithm"


void getRunsForPeriod(TString period = "LHC10b", Int_t * runs = 0, Int_t nruns = 0)
{
    std::ifstream file(period + ".txt");

    std::vector<int> v; // 
    std::copy(std::istream_iterator<int>(file), std::istream_iterator<int>(),
                                                 std::back_inserter(v));

    std::cout << "Reading: " << v.size() << " runs." << std::endl;

}