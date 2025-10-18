#include <iostream>
#include "stdio.h"

int main() {
    std::cout << "What's your favorite number? ";
    int fav_number;
    scanf("%d", &fav_number);
    int evil_number = fav_number * -1;
    std::cout << "Your favorite number if it was evil: " << evil_number << " >:3\n";
    return 0;
}