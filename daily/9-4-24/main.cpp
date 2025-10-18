#include <iostream>
#include <cmath>

int main() {
    int n = 1000;

    for (int i = 1; i <= n; i++) {
        float ev = 0;

        for (int x = 0; x < i; x++) {
            ev += i;
        }

        ev *= 6;
        ev = pow(ev, -2);

        std::cout << "   " << ev << std::endl;
    }
}