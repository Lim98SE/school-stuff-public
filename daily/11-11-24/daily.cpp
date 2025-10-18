#include <iostream>

void printBananas() {
    for (int i = 0; i < 3; i++) {
        std::cout << "Banana dance! 🍌" << std::endl;
    }
}

void snailCount() {
    int numSnails = 3;
    int currentSnail = 0;

    while (currentSnail < numSnails) {
        std::cout << "Snail #" << currentSnail + 1 << std::endl;
        currentSnail++;
    }
}

void checkCarrots() {
    int carrots;
    std::cout << "How many carrots do you have? ";
    std::cin >> carrots;

    if (carrots > 3) {
        std::cout << "Too many carrots!";
    } else {
        std::cout << "Not enough carrots.";
    }
}

int main() {
    printBananas();
    snailCount();
    checkCarrots();
}