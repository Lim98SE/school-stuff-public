#include <vector>
#include <string>

std::vector<std::string> enemy_types = {
    "Bad Enemy",
    "What the F**k"
};

class item {
    public:
    std::string name;
    int mhpmod;
    int atkmod;
    int defmod;
    int magmod;
};

std::vector<item> item_ids = {
    item{
        "Cool Sword",
        100,
        100,
        100,
        100
    },
    item{
        "Segfault Sword",
        100,
        1000000,
        0,
        100
    },
};

class enemy {
    public:
    double health;
    int attack;
    int def; // this / 100 is how much damage the player gets to deal, so 50 is half as much
    int drop = -1;
    int type; // only used for the name

    void damage(int attack_power) {
        double actual_atk = attack_power * (def / 100);
        health -= actual_atk;
    }
};

class room {
    public:
    int exits[4]; // North, East, South, West
    std::vector<enemy> enemies;
    std::vector<item> items;
    std::string description;
};

std::vector<room> rooms = {
    room{{1, 0, 0, 0},
    {enemy{
        10,
        1,
        200,
        0,
        0
    }},
    {},
    "Cool Room"},

    room{{1, 1, 0, 1},
    {enemy{
        10,
        1,
        100,
        0,
        0
    }},
    {},
    "Lame Room"}
};