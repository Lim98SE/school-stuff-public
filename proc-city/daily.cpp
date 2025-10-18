#include <iostream>
#include <string>

int main() {
    std::string inp;

    while (inp != "BOOP") {
        std::getline(std::cin, inp);
        if (inp == "BOOP") {
            break;
        }
        std::cout << "FORGLE" << std::endl;
    }

    return 0;
}