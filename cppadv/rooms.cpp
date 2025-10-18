#include <string>
#include "include/Color.hpp"
#define TRANSPARENT Color{0, 0, 0, 0}
using namespace std;

// North, East, South, West

std::vector<std::vector<int>> rooms = {
    { 0, 0, 1, 1 },
    { 1, 0, 0, 1 },
    { 0, 1, 1, 0},
    { 0, 1, 0, 1},
    { 0, 1, 0, 1},
    { 1, 1, 0, 1},
    {1, 0, 1, 0},
    {1, 0, 1, 0},
    {1, 0, 1, 0},
    {1, 0, 1, 0},
    {1, 0, 1, 0},
    {1, 0, 1, 0},
    {1, 0, 1, 0},
    {1, 1, 1, 0},
};

std::vector<int> room_pickups = {
    -1,
    -1,
    1
};

std::vector<int> dialog_pointers = {
    0,
    1,
    4
};

std::vector<std::vector<float>> room_positions = {
    {0, 0},
    {0, 1},
    {1, 1},
    {1, 2},
    {1, 3},
    {1, 4},
    {1, 0},
    {2, 0},
    {3, 0},
    {4, 0},
    {5, 0},
    {6, 0},
    {7, 0},
    {8, 0},
};

std::vector<Color> room_colors = {
    RED,
    RED,
    GRAY,
    GRAY,
    BLUE,
    BLUE,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK
};

std::vector<Color> room_floors = {
    BLACK,
    BLACK,
    BLACK,
    WHITE,
    WHITE,
    WHITE,
    WHITE,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK
};

std::vector<Color> room_tops {
    BLACK,
    TRANSPARENT,
    Color{0, 0, 0, 127},
    TRANSPARENT,
    WHITE,
    WHITE,
    WHITE,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK
};

std::vector<int> room_wall_textures = {
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
};

std::vector<int> room_floor_textures = {
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
};

std::vector<int> room_top_textures = {
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
};