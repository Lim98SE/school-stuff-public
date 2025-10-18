#include <iostream>
#include <any>

class Node {
    public:
    int value;
    int uuid;
    Node* next = NULL;

    Node(int v, int u) {
        value = v;
        uuid = u;
    }
};

int main() {
    Node n1 = Node(0, 0);
    Node n2 = Node(5, 1);
    Node n3 = Node(22, 2);
    n1.next = &n2;
    n2.next = &n3;

    int index = 0;
    Node current = n1;
    std::cout << current.value << std::endl;

    while (current.next != NULL) {
        current = *current.next;
        std::cout << current.value << std::endl;
    }

    return 0;
}