#include <vector>
#include <any>
#include <iostream>

void push(std::vector<int>* stack, int item) {
    stack->push_back(item);
}

int pop(std::vector<int>* stack) {
    int item = stack->at(stack->size() - 1);
    stack->pop_back();
    return item;
}

void print_all(std::vector<int>* stack) {
    for (auto i: *stack) {
        std::cout << i << " ";
    }

    std::cout << std::endl;
}

std::vector<int> stack = {0, 1, 2, 3};

int main() {
    print_all(&stack);
    push(&stack, 5);
    print_all(&stack);
    int popped = pop(&stack);
    print_all(&stack);
    std::cout << "Popped " << popped << std::endl;
}