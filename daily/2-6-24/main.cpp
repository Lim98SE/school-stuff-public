#include <iostream>
#include <string>

class Car {
    private:
        int engineHealth = 0;
        int transmissionHealth = 0;
        int lastServiceDate = 8302008;
    
        friend class Mechanic;
    
        public:
            void drive() {
                engineHealth = rand() % 4;
                transmissionHealth = rand() % 4;
            }
};

class Mechanic {
    public:
        void diagnose(Car &car) {
            std::cout << "--- REPORT ---\n";
            std::cout << "Engine health is: ";
            switch (car.engineHealth) {
                case 0: std::cout << "Perfectly fine\n"; break;
                case 1: std::cout << "Minor issues\n"; break;
                case 2: std::cout << "Moderate issues\n"; break;
                case 3: std::cout << "SEVERE ISSUES\n"; break;
            }

            std::cout << "Transmission health is: ";
            switch (car.transmissionHealth) {
                case 0: std::cout << "Perfectly fine\n"; break;
                case 1: std::cout << "Minor issues\n"; break;
                case 2: std::cout << "Moderate issues\n"; break;
                case 3: std::cout << "SEVERE ISSUES\n"; break;
            }
            std::cout << "Last service date was: " << car.lastServiceDate << std::endl;
        }

        void fix(Car &car) {
            car.engineHealth = 0;
            car.transmissionHealth = 0;
        }
};

int main() {
    srand(time(NULL));
    Car hondaCivic;

    hondaCivic.drive();

    Mechanic jesse;

    jesse.diagnose(hondaCivic);
    jesse.fix(hondaCivic);
    jesse.diagnose(hondaCivic);

    return 0;
}