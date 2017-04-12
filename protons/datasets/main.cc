#include "vector"
#include "iterator"
#include "fstream"
#include "iostream"
#include "algorithm"


int main(int argc, char const *argv[])
{
    std::ifstream file("LHC10d.txt");

    std::vector<int> v; // 
    // std::copy(std::istream_iterator<int>(file), std::istream_iterator<int>());
    std::copy(std::istream_iterator<int>(file), std::istream_iterator<int>(),
                                                 std::back_inserter(v));


    std::cout << "Output n: " << v.size() << std::endl;
    return 0;
}
