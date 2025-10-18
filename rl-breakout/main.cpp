#include "include/raylib-cpp.hpp"
#include "classes.cpp"
#include <vector>
#include <iostream>

std::vector<Block> blocks;
int playfield_x = 5;
struct Vec2 block_size = {128, 32};
int blockOffset = 4;
Block paddle;

std::vector<Color> colors = {
    Color{255, 0, 0, 255},
    Color{255, 255, 0, 255},
    Color{255, 0, 255, 255},
    Color{0, 255, 0, 255},
    Color{0, 255, 255, 255},
    Color{0, 0, 255, 255}
};

Color get_color() {
    int index = GetRandomValue(0, colors.size() - 1);

    for (int i = 0; i < GetRandomValue(0, 1000000); i++) {
        GetRandomValue(0, 1);
    }

    return colors[index];
}

std::vector<Block> make_playfield(int rows) {
    std::vector<Block> output;

    for (int y = 0; y < rows; y++) {
        for (int x = 0; x < playfield_x; x++) {
            output.push_back(
                Block{
                    Hitbox{
                        Vec2{((float)x * block_size.x) + (blockOffset * x), ((float)y * block_size.y) + (blockOffset * y)},
                        block_size
                    },
                    get_color()
                }
            );
        }
    }

    return output;
}

Ball ball;

void break_block(Block &block) {
    Block found;
    int index = 0;
    for (auto b: blocks) {
        index += 1;
        if (b.hitbox.position.x == block.hitbox.position.x) {
            if (b.hitbox.position.y == block.hitbox.position.y) {
                found = b;
                break;
            }
        }
    }

    blocks[index - 1].hitbox.enabled = false;
}

int main() {
    SetRandomSeed(time(NULL));
    InitAudioDevice();

    int screenWidth = 650;
    int screenHeight = 800;

    Sound bounceSfx = LoadSound("break.wav");
    Sound dieSfx = LoadSound("die.wav");
    Sound breakSfx = LoadSound("bounce.wav");

    ball.hitbox.size = {16, 16};
    ball.hitbox.position.x = (screenWidth / 2) - (ball.hitbox.size.x / 2);
    ball.hitbox.position.y = screenHeight - ball.hitbox.size.y - 32;
    ball.velocity.y = -4;

    paddle.color = Color{255, 255, 255, 255};
    paddle.hitbox.size = {256, 16};
    paddle.hitbox.position = {0, screenHeight - ball.hitbox.size.y - 8};
    paddle.hitbox.enabled = true;

    blocks = make_playfield(8);

    raylib::Window window(screenWidth, screenHeight, "Breakout!");

    float averageFps = 0.0;
    int fpsReadings = 0;

    // SetTargetFPS(60);

    while (!window.ShouldClose()) {
        BeginDrawing();

        window.ClearBackground(BLACK);

        ball.move();

        paddle.draw();

        paddle.hitbox.position.x = GetMousePosition().x - (paddle.hitbox.size.x / 2);
        for (auto block: blocks) {
            block.draw();

            if (block.hitbox.collision(&ball.hitbox)) {
                ball.velocity.y *= -1;
                break_block(block);
                PlaySound(breakSfx);
            }
        }

        if (ball.hitbox.position.x < 0 || ball.hitbox.position.x > screenWidth) {
            ball.velocity.x *= -1;
            PlaySound(bounceSfx);
        }

        if (ball.hitbox.position.y < 0) {
            ball.velocity.y *= -1;
            PlaySound(bounceSfx);
        }

        if (paddle.hitbox.collision(&ball.hitbox)) {
            ball.velocity.y *= -1;

            ball.velocity.x = ((ball.hitbox.position.x - paddle.hitbox.position.x) - (paddle.hitbox.size.x / 2)) / 12;
            PlaySound(bounceSfx);
        }

        if (ball.hitbox.position.y > screenHeight || GetKeyPressed()) {
            PlaySound(dieSfx);
            ball.velocity = {0, -4};
            ball.hitbox.position.x = (screenWidth / 2) - (ball.hitbox.size.x / 2);
            ball.hitbox.position.y = screenHeight - ball.hitbox.size.y - 32;
        } 

        ball.draw();

        GetFPS()

        EndDrawing();
    }

    // UnloadTexture() and CloseWindow() are called automatically.

    return 0;
}