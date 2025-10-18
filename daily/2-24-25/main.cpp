#include <iostream>

// problem c

void swap(int* x, int* y) {
    int buffer = *x;
    *x = *y;
    *y = buffer;
}

int main() {
    int a = 0;
    int b = 285875;

    std::cout << a << " " << b << std::endl;

    swap(&a, &b);

    std::cout << a << " " << b << std::endl;

    return 0;
}