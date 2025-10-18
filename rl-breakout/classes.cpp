#include "include/raylib-cpp.hpp"

struct RGB {
    int r;
    int g;
    int b;
};

struct Vec2 {
    float x;
    float y;
};

class Hitbox {
    public:
    struct Vec2 position;
    struct Vec2 size;
    bool enabled = true;

    bool collision(Hitbox* ptr_other) {
        if (!enabled) {
            return false;
        }

        Hitbox other = *ptr_other;
        if (other.position.x > position.x && other.position.x < position.x + size.x) {
            if (other.position.y > position.y && other.position.y < position.y + size.y) {
                return true;
            }
        }

        return false;
    }
};

class Ball {
    public:
    Hitbox hitbox;
    struct Vec2 velocity;
    struct RGB color;

    void move() {
        hitbox.position.x += velocity.x;
        hitbox.position.y += velocity.y;
    }

    void draw() {
        DrawRectangle(hitbox.position.x, hitbox.position.y, hitbox.size.x, hitbox.size.y, Color{255, 0, 0, 255});
    }
};

class Block {
    public:
    Hitbox hitbox;
    Color color;

    void draw() {
        if (!hitbox.enabled) { return; }
        DrawRectangle(hitbox.position.x, hitbox.position.y, hitbox.size.x, hitbox.size.y, color);
    }
};