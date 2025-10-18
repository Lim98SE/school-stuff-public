#include <iostream>

int main() {
    srand(time(NULL));

    for (int i = 0; i < 1000000; i++) {
        for (int r = 0; r < (int)(rand() % 20); i++) {
            std::cout << " ";
        }

        std::cout << char(3);
    }
}