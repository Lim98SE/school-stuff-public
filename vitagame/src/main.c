#include <stdio.h>
#include <stdbool.h>
#include "../include/SDL2/SDL.h"

const int SCR_WIDTH = 960;
const int SCR_HEIGHT = 544;

int WinMain() {
    SDL_Window* window = NULL;

    SDL_Surface* canvas = NULL;

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("%s\n", SDL_GetError());
    }

    window = SDL_CreateWindow( "SDL Tutorial", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCR_WIDTH, SCR_HEIGHT, SDL_WINDOW_SHOWN );

    if (window == NULL) {
        printf("%s\n", SDL_GetError());
    }

    canvas = SDL_GetWindowSurface(window);
    SDL_FillRect(canvas, NULL, SDL_MapRGB(canvas->format, 0x00, 0x40, 0xFF));
    SDL_UpdateWindowSurface(window);

    SDL_Event e; bool quit = false; while( quit == false ){ while( SDL_PollEvent( &e ) ){ if( e.type == SDL_QUIT ) quit = true; } }

    return 0;
}