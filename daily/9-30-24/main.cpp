#include <iostream>

int sumDigits(int n) {
    int out = 0;

    for (n; n > 0; n--) {
        out += n;
    }

    return out;
}

inline float area(float width, float height) { return width * height; }

int main() {
    std::cout << sumDigits(3) << std::endl;
    std::cout << area(5, 5) << std::endl;
}





