#include <iostream>
#include <stdlib.h>
#include <vector>

template <typename Iterator, typename Predicate> Iterator mymax(Iterator first, Iterator last, Predicate pred) {
    Iterator max = first;
    while (first != last)
    {
        int cmp = pred(*first, *max);
        if (cmp)
            max = first;
        first++;
    }
    return max;
}

int gt_int(const int &p, const int &q) {
    return p > q;
}

int gt_str(const char &p, const char &q) {
    return p > q;
}

int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
int main(){
    const int* maxint = mymax(&arr_int[0],
    &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int);
    std::cout <<*maxint <<"\n";

    std::string str("Suncana strana ulice");
	auto result = mymax(str.begin(), str.end(), gt_str);
    std::cout << *result <<"\n";
}