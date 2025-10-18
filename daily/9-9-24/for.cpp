#include <iostream>

int main() {
    for (int i = 0; i <= 18; i++) {
        std::cout << i << std::endl;
    }

    std::cout << "---------------\n";

    for (int i = 25; i <= 45; i++) {
        std::cout << i << std::endl;
    }

    std::cout << "---------------\n";

    for (int i = 40; i <= 80; i += 4) {
        std::cout << i << std::endl;
    }

    std::cout << "---------------\n";

    for (int i = 12; i >= -6; i -= 3) {
        std::cout << i << std::endl;
    }
}