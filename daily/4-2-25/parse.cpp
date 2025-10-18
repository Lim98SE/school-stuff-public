#include <cstring>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <vector>

int pointer = 0;

std::vector<unsigned char> buffer;

int read_8() {
    pointer++;
    return buffer[pointer];
}

int main() {
    std::fstream file;

    uint8_t x = 40;

    // thanks a lot to https://www.coniferproductions.com/posts/2022/10/25/reading-binary-files-cpp/ for help with this code

    file.open("song.bin", std::ios::binary | std::ios::in);
    file.seekg(0, std::ios_base::end);
    auto length = file.tellg();
    file.seekg(0, std::ios_base::beg);

    file.read(reinterpret_cast<char*>(buffer.data()), length);

    std::cout << "read " << length << " bytes\n";

    file.close();

    return 0;
}