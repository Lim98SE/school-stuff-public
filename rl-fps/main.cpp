#include "include/raylib-cpp.hpp"

int main() {
    const int screenWidth = 1280;
    const int screenHeight = 720;

    raylib::Window window(screenWidth, screenHeight, "Framerate");

    while (!window.ShouldClose()) {
        BeginDrawing();

        window.ClearBackground(BLACK);

        DrawFPS(0, 0);

        EndDrawing();

    }

    return 0;
}