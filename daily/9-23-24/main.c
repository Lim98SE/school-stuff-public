// question 1: can represent 16 numbers with 4 bits (0 - 15)
// question 2: all but C
// question 3: when provided with a false statement by default it's not executed, so D
// question 4: only 0 is considered false
// question 5 is in the code
// question 6: zero, so A
// question 7: A and C
// question 8 is in the code
// question 9: cp ./icel.c ~/106/
// question 10: -1 gives 19 101, 100 gives 20 101
// question 11 is in the code
// question 12 is in the code
// question 13 is in the code

#include "stdio.h"

int main() {

    // question 5

    float y = 18.634237;

    printf("%f\n", y);

    // question 8

    y *= 3;
    y *= 4;

    // question 11

    printf("Robert \"Bobby\" (hill\?\?\?\?\?)\n"); // compiler was warning me about "trigraphs" so i escaped the question marks

    // question 12

    int a, b;
    a = 1;
    b = 2;

    while (a < 10) {
        printf("%d %d\n", a, b);
        a++; b++;
    }

    // question 13

    char c = 'x';

    switch (c) {
        case 'a':
            printf("Case 1\n");
            break;
        
        case 'm':
            printf("Case 2\n");
            break;
        
        default:
            printf("Other case\n");
            break;
    }
}