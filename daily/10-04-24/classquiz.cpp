#include <iostream>
#include <string>

class Student {
    private:
        std::string name;
        int mathGrade;
        int scienceGrade;
        int englishGrade;
    
    public:
        Student(std::string myName, int math, int science, int english) {
            name = myName;
            mathGrade = math;
            scienceGrade = science;
            englishGrade = english;
        }

        inline float getAverage() { return (mathGrade + scienceGrade + englishGrade) / 3; }
        void printReport() {
            std::cout << "Student Name: " << name << " | Math Grade: " << mathGrade << " | Science Grade: " << scienceGrade << " | English Grade: " << englishGrade << " | Average Grade: " << getAverage() << std::endl;
        }
};

int main() {
    Student student = Student(":3", 10, 50, 100);
    student.printReport();
}

