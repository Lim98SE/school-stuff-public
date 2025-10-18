#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <any>
#include <format>
#include <math.h>
#include "map.cpp"

int state = 0;

// state 0: map
// state 1: fight

std::vector<std::vector<std::string>> normal_aliases = {
    {
        "go",
        "g",
        "walk",
        "move",
        "m"
    },
    {
        "north",
        "n"
    },
    {
        "east",
        "e"
    },
    {
        "south",
        "s"
    },
    {
        "west",
        "w"
    },
    {
        "look",
        "cr"
    },
    {
        "changestate",
        "cs"
    }
};

std::vector<std::vector<std::string>> battle_aliases = {
    {
        "attack",
        "fight",
        "a",
        "f"
    },
    {
        "use",
        "u"
    },
    {
        "inventory",
        "i"
    }
};

std::vector<std::vector<std::string>> get_commands(int mode) {
    std::vector<std::vector<std::string>> current_aliases;
    switch (mode) {
    case 0:
        current_aliases = normal_aliases;
        break;
    
    case 1:
        current_aliases =  battle_aliases;
        break;
    }

    return current_aliases;
}

int current_room = 0;

std::vector<std::string> split(std::string s, std::string delimiter) { // https://stackoverflow.com/questions/14265581/parse-split-a-string-in-c-using-string-delimiter-standard-c
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    std::string token;
    std::vector<std::string> res;

    while ((pos_end = s.find(delimiter, pos_start)) != std::string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}

std::string make_lowercase(std::string data) { // stackoverflow my beloved
    std::transform(data.begin(), data.end(), data.begin(),
        [](unsigned char c){ return std::tolower(c); });
    
    return data;
}

bool move(int to) {
    if (to > 3 || to < 0) {
        return current_room;
    }

    current_room = rooms[current_room].exits[to];

    return current_room;
}

int cmd_to_index(std::string command) {
    int index = 0;
    for (auto x: get_commands(state)) {
        for (auto y: x) {
            if (y == command) {
                return index;
            }
        }

        index++;
    }

    return -1;
}

int mod(int a, int b) { // https://stackoverflow.com/questions/7594508/why-does-the-modulo-operator-result-in-negative-values
    return (b + (a % b)) % b;
}

bool running = true;
int direction;
int idx = 0;
int health = 10;
int magic = 5;
int defense = 100;
int attack = 1;
int turns = 0;

void breif(std::vector<enemy> enemies) {
    std::cout << "In battle with:\n";

    int enemy_id = 0;

    for (auto i: enemies) {
        
        std::cout << enemy_types[i.type] << " with " << round(i.health) << " health (ID: " << enemy_id + 1 << ")\n";
        enemy_id += 1;
    }
}

void gs0(std::vector<std::string> command) {
    int cmd_index = cmd_to_index(command[0]);

    switch (cmd_index) {
        case 0: // Go
            direction = cmd_to_index(command[1]) - 1; // get index into array
            current_room = move(direction);
            break;
        
        case 5:
            std::cout << "You are in: " << rooms[current_room].description << std::endl;

            idx = 0;

            for (auto i: rooms[current_room].exits) {
                if (i != current_room) {
                    int exit_direction = mod(idx, 4);
                    std::cout << "There is an exit to the " << get_commands(state)[exit_direction + 1][0] << std::endl;
                }

                idx += 1;
            }

            break;
        
        case 6:
            state = std::stoi(command[1]);

            if (state == 1) {

                turns = 0;
                breif(rooms[current_room].enemies);
            }

            break;
        
        default: // Error case
            std::cout << "Unknown command: " << command[0] << std::endl;
            std::cout << "CMDIDX: " << cmd_index << std::endl;
    }
}

std::vector<enemy> get_alive_enemies(std::vector<enemy> enemies) {
    std::vector<enemy> actual_enemies;

    for (auto i: enemies) {
        if (i.health > 0) {
            actual_enemies.push_back(i);
        }
    }

    return actual_enemies;
}

void gs1(std::vector<std::string> command) {
    int cmd_index = cmd_to_index(command[0]);
    std::vector<enemy> enemies = rooms[current_room].enemies;
    std::vector<enemy> actual_enemies;

    actual_enemies = get_alive_enemies(enemies);

    if (actual_enemies.size() == 0) {
        state = 0;
        std::cout << "You won the battle!\n";
        return;
    }

    switch (cmd_index) {
        case 0:
            int enemy_index = std::stoi(command[1]) - 1;

            rooms[current_room].enemies[enemy_index].damage(attack);

            actual_enemies = get_alive_enemies(rooms[current_room].enemies);

            if (rooms[current_room].enemies[enemy_index].health <= 0) {
                std::cout << "Slayed the " << enemy_types[rooms[current_room].enemies[enemy_index].type] << "\n";

                if (rooms[current_room].enemies[enemy_index].drop != -1) {
                    std::cout << "They were holding a " << item_ids[rooms[current_room].enemies[enemy_index].drop].name << "!\n";
                }
            } else {
                std::cout << "They still have " << rooms[current_room].enemies[enemy_index].health << " HP left.\n";
            }

            if (actual_enemies.size() == 0) {
                state = 0;
                std::cout << "You won the battle!\n";
                return;
            }
    }

    turns += 1;
}

int main() {
    while (running) {
        std::cout << "Command: ";
        std::string input;
        input = make_lowercase(input);
        std::getline(std::cin, input);
        std::vector<std::string> command = split(input, " ");

        switch (state) {
            case 0:
                gs0(command);
                break;
            
            case 1:
                gs1(command);
                break;
        }

    }

    return 0;
}