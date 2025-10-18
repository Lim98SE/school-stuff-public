#include "include/raylib-cpp.hpp"
#include <string>
#include <iostream>

int cookies = 0;
int cookies_persecond = 0;
int cookies_perclick = 1;

int cookie_ps_cost = 5;
int cookie_pc_cost = 30;

bool point_colliding_oneaxis(int point, int test, int test_width) {
    return point >= test && point <= test + test_width;
}

bool point_collision(Vector2 point, Vector2 test, Vector2 test_size) {
    return point_colliding_oneaxis(point.x, test.x, test_size.x) && point_colliding_oneaxis(point.y, test.y, test_size.y);
}

bool purchase(int cost, int* original_cost) {
    if (cost > cookies) {
        return false;
    }

    *original_cost *= 1.5;

    cookies -= cost;
    return true;
}

int main() {
    const int screen_width = 1024;
    const int screen_height = 768;

    raylib::InitWindow(screen_width, screen_height, "rl-cookie");

    SetExitKey(KEY_NULL);

    raylib::Font main_font = LoadFont("font.ttf");

    Vector2 cookie_position = {128, 128};
    Texture2D cookie_sprite = LoadTexture("assets/cookie.png");

    Color cookie_color;
    cookie_color = WHITE;

    ToggleBorderlessWindowed();

    SetTargetFPS(1000);

    while (!WindowShouldClose()) {
        if ((int)(GetTime() * 1000) % 1000 == 0) {
            cookies += cookies_persecond * cookies_perclick;
        }

        BeginDrawing();

        ClearBackground(WHITE);

        DrawTextPro(main_font, std::to_string(cookies) + " Cookies", Vector2{0, 0}, Vector2{0, 0}, 0, 32, 0, BLACK);
        DrawTextPro(main_font, std::to_string(cookie_ps_cost) + " Cookies for a cursor", Vector2{0, 32}, Vector2{0, 0}, 0, 32, 0, BLACK);
        DrawTextPro(main_font, std::to_string(cookie_pc_cost) + " Cookies for a click upgrade", Vector2{0, 64}, Vector2{0, 0}, 0, 32, 0, BLACK);

        if (point_collision(GetMousePosition(), cookie_position, {256, 256})) {
            if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                cookies += cookies_perclick;
            }
        }

        if (IsKeyPressed(KEY_A)) {
            if (purchase(cookie_ps_cost, &cookie_ps_cost)) {
                cookies_persecond += 1;
            }
        }

        if (IsKeyPressed(KEY_S)) {
            if (purchase(cookie_pc_cost, &cookie_pc_cost)) {
                cookies_perclick += 1;
            }
        }

        DrawTexture(cookie_sprite, cookie_position.x, cookie_position.y, cookie_color);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}