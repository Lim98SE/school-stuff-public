#include "include/raylib-cpp.hpp"// load raylib

int front_x = 0; // stores the position of the front of the card
bool sliding = false; // "sliding" is the state the card is put into when it slides off the screen with no input
Vector2 window_size = Vector2{512, 768}; // this is the window size

int main() {
    raylib::InitWindow(512, 768, "CPPCON Thank You Card"); // init a window 512x768 with a title of "CPPCON Thank You Card"

    Texture2D front = LoadTexture("front.png"); // load texture "font.png" (put AFTER InitWindow or it segfaults)
    Font font = LoadFont("font.ttf"); // font font lol

    SetTargetFPS(60); // set the target FPS to 60

    while (!WindowShouldClose()) { // while running
        BeginDrawing(); // begin the frame

        ClearBackground(WHITE); // clear the background

        // this long line of code kills me inside
        DrawTextEx(font, "Hi! Thank you so much for\n\nletting us come!\n\nI'm still a newcomer to C++\n\nbut I really enjoyed the\n\nstuff I saw.\n\nA lot of it was really\n\nconfusing, but super\n\ninteresting at the\n\nsame time?\n\nPlus, it was neat\n\nbeing able to hang\n\nout in that hotel room\n\nfor a bit.\n\n\n\nOnce again, thank you so\n\nvery much for letting all of\n\nus here at SCHOOL Game\n\ndesign come to CPPCon!\n\nI hope we'll be able\n\nto come back next year!\n\n\n\n-Liam LASTNAME", Vector2{8, 8}, 32, 2, BLACK);
        // it draws the text
        // it's \n\n instead of just \n because DrawText() is just. weird

        if (IsMouseButtonDown(MOUSE_BUTTON_LEFT) && !sliding) { // so if the mouse is pressed or not sliding
            front_x = GetMousePosition().x - window_size.x; // calculate the front x based on the RIGHT corner, NOT the left (that's why the window_size.x is there)
            front_x = Clamp(front_x, -window_size.x, 0); // clamp it between the edge of the window and 0 so it can't go off the right end

            if (front_x < -200) { // if it's 200px away from its starting point
                sliding = true; // set it to slide
            }
        } else if (sliding) {
            front_x -= 60; // if sliding, move it by 60px a frame
        }

        DrawTexture(front, front_x, 0, WHITE); // draw the front of the card at (front_x, 0) with no tint

        EndDrawing(); // end the frame
    }

    // raylib automatically closes the window so that's it
}