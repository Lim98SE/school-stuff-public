#include <iostream>

struct data {
    float pos[2];
};

struct data midpoint(float x1, float y1, float x2, float y2) {
    struct data r;
    float mx = (x1 + x2) / 2;
    float my = (y1 + y2) / 2;

    r.pos[0] = mx;
    r.pos[1] = my;

    return r;
}

int main() {
    float x1;
    float y1;
    float x2;
    float y2;

    std::cout << "X1: ";
    std::cin >> x1;

    std::cout << "Y1: ";
    std::cin >> y1;

    std::cout << "X2: ";
    std::cin >> x2;

    std::cout << "Y2: ";
    std::cin >> y2;

    struct data m = midpoint(x1, y1, x2, y2);

    std::cout << "Pos 1: " << x1 << ", " << y1 << std::endl;
    std::cout << "Pos 2: " << x2 << ", " << y2 << std::endl;
    std::cout << "Midpoint: " << m.pos[0] << ", " << m.pos[1] << std::endl;

    return 0;
}