#include <iostream>
#include <string>

void truck_weight_check(int load_weight) {
    if (load_weight > 1200) {
        std::cout << "Overweight!";
        return;
    }
    std::cout << "Within limit.";
}

int get_ticket_price(int visitor_age) {
    if (visitor_age < 10) {
        return 8;
    } else if (visitor_age < 60) {
        return 18;
    }

    return 12;
}

void verify_username() {
    std::string username;

    while (username != "CodeMaster123") {
        getline(std::cin, username);
    }

    std::cout << "Access granted!";
}

void docking_countdown(){
    for (int i = 20; i > 0; i -= 3) {
        std::cout << i << std::endl;
    }
}

void school_zone_signal(std::string color){
    if (color == "Red") {
        std::cout << "Stop";
    } else if (color == "Yellow") {
        std::cout << "Be ready";
    } else if (color == "Green") {
        std::cout << "Proceed";
    } else {
        std::cout << "Weird school signal but ok";
    }
}

int main() {
    docking_countdown();
    truck_weight_check(1200);
    truck_weight_check(1201);
    school_zone_signal("Red");
    school_zone_signal("Yellow");
    school_zone_signal("Green");
    school_zone_signal("Blue");
    get_ticket_price(0);
    get_ticket_price(18);
    get_ticket_price(200);
    verify_username();
}