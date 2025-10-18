#include <iostream>
#include <windows.h>
#include <fstream>
#include <string>
#include <vector>
#include <stdlib.h> 

char word[16] = "";
int word_length = 5;
bool guesses[16];

std::vector<std::string> categories = {
    "PROGRAMMING LANGUAGES", // 0
    "SOFTWARE",              // 1
    "HARDWARE",              // 2
    "PEOPLE",                // 3
    "MISC.",                 // 4
    "TOOLS",                 // 5
    "GAMES",                 // 6
};

#define G4 392
#define Fb4 370
#define B4 494
#define C5 523
#define D5 587

bool won = false;

int remaining_guesses = 10;

void pick_word() {
    int word_count = 0;
    std::ifstream file("words.txt");
    std::string raw_wc;
    std::getline(file, raw_wc);
    word_count = std::stoi(raw_wc);

    int word_index = rand() % word_count;
    int category = -1;

    for (int i = 0; i < word_count; i++) {
        std::string line;
        std::getline(file, line);
        std::string buffer = "";
        int num_start_idx = 0;
        for (int x = line.length(); x--; x <= 0) {
            if (line[x] == '/') {
                num_start_idx = x;
                break;
            }
        }

        if (i == word_index) {
            category = std::atoi(&line[0]);
            line.erase(line.begin());
            std::copy(line.begin(), line.end() - 1, word);
            word_length = num_start_idx - 1;
        }
    }

    std::cout << "CATEGORY: " << categories[category] << std::endl;
}

char filter_char(char inp) {
    unsigned char real_input = (unsigned char)inp;

    if (real_input >= 97 && real_input <= 122) {
        real_input -= 32;
    } else {
        return inp;
    }

    return (char)real_input;
}

void incorrect_beep() {
    Beep(466, 150);
    Beep(392, 300);
}

void correct_beep() {
    Beep(293, 100);
    Beep(330, 100);
    Beep(392, 100);
    Beep(494, 100);
}

void you_win() {
    std::cout << "YOU WIN!!!\n";
    std::cout << "The word was " << word << std::endl;

    Beep(G4, 146);
    Beep(Fb4, 97);
    Beep(G4, 97);
    Sleep(49);
    Beep(B4, 97);
    Sleep(121);
    Beep(C5, 97);
    Sleep(24);
    Beep(B4, 97);
    Sleep(146);
    Beep(D5, 97);
}

void evaluate(char guess) {
    bool was_in_word = false;
    for (int i = 0; i < word_length; i++) {
        if (word[i] == guess) {
            guesses[i] = true;
            was_in_word = true;
        }
    }

    if (was_in_word) {
        correct_beep();
        return;
    }

    remaining_guesses -= 1;
    incorrect_beep();
    std::cout << "No " << guess << std::endl;
    return;
}

void print_guess() {
    for (int i = 0; i < word_length; i++) {
        if (!guesses[i]) {
            std::cout << "?";
        }

        else {
            std::cout << word[i];
        }
    }
    std::cout << std::endl;
}

void print_status() {
    std::cout << remaining_guesses << " guesses remaining\n";
    print_guess();
}

void get_guess() {
    char guess;
    std::cout << "? ";
    std::cin >> guess;
    guess = filter_char(guess);
    evaluate(guess);

    won = true;

    for (int i = 0; i < word_length; i++) {
        won = won & guesses[i];
    }

    if (won) {
        you_win();
    }
}

int main() {
    system("cls");
    std::cout << "NERD HANGMAN\n\n";
    srand(time(NULL));
    std::cout << "Choosing word... ";
    pick_word();
    std::cout << "Done!\n";

    while (remaining_guesses > 0 && !won) {
        print_status();
        get_guess();
    }

    if (won) {
        return 0;
    }

    std::cout << "You lose...\n";
    std::cout << "The word was " << word << std::endl;
    for (int i = 0; i < 50; i++) {
        Beep(600 - (i * 10), 50);
    }
    return 0;
}