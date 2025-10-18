#include <iostream>
#include "stdio.h" // gets() is nice
#include <string>

int main() {
    int index = 6;

    while (index <= 36) {
        std::cout << index << std::endl;
        index += 3;
    }

    std::string input;
    std::string condition = "banana";

    while (input != condition) {
        std::cout << "Apple\n";
        std::getline(std::cin, input);
    }

    int new_input;

    do {
        std::cout << "Number: ";
        std::cin >> new_input;
        std::cout << new_input * new_input;
    } while (new_input != 0);

}