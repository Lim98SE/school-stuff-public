#include <iostream>
#include "include/SDL2/SDL.h"

SDL_Rect generate_rect(int x, int y, int w, int h) {
    SDL_Rect rect;
    rect.x = x;
    rect.y = y;
    rect.w = w;
    rect.h = h;
    return rect;
}

SDL_Window *window;
SDL_Renderer *renderer;

int WinMain() {
    if (SDL_Init(SDL_INIT_VIDEO)) {
        std::cout << "Window init\'d" << std::endl;
    } 
    SDL_CreateWindowAndRenderer(640, 480, 0, &window, &renderer);

    if (!window) {
        std::cout << "Window failed to init" << std::endl;
        return -1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, 0, 0);
    
    while (true) {
        SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
        SDL_RenderClear(renderer);
        SDL_RenderFillRect(renderer, )
        SDL_RenderPresent(renderer);
    }

    return 0;
}