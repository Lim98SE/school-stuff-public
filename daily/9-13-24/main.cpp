#include <iostream>
#include <string>

int main() {
    std::string input;

    std::cout << "Do you like fish? ";
    std::cin >> input;

    if (input == "y") {
        std::cout << "Blub blub!\n";
    }

    std::cout << "How many fish do you have? ";
    std::cin >> input;
    int numfish = std::atoi(input.c_str());

    if (numfish < 5) {
        std::cout << "You don't have enough fish.\n";
    } else {
        std::cout << "You're fishy.\n";
    }
}