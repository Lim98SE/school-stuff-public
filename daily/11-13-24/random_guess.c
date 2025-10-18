#include "stdio.h"

int getRandomNumber() {
    return (rand() % 100) + 1;
}

int main() {
    int guess;
    int answer = getRandomNumber();

    printf("Answer is %i\n", answer);
}