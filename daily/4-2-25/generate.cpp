#include <cstring>
#include <fstream>
#include <iostream>
#include <cstdint>

uint16_t length = 6;

const uint8_t notes[] = {
    44,
    0,
    88,
    0,
    44,
    0
};

const uint16_t durations[] = {
    1000,
    250,
    1000,
    250,
    2000,
    250
};

int main() {
    std::fstream file;

    uint8_t x = 40;

    file.open("song.bin", std::ios::binary | std::ios::out);

    file.write(reinterpret_cast<char*>(&length), sizeof(length));

    for (int i = 0; i < sizeof(notes) / sizeof(uint8_t); i++) {
        uint8_t freq = notes[i];
        uint16_t duration = durations[i];
        file.write(reinterpret_cast<char*>(&freq), sizeof(freq));
        file.write(reinterpret_cast<char*>(&duration), sizeof(duration));
    }

    file.close();

    return 0;
}