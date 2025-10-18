#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cctype>
#include "rooms.cpp"
#include "items.cpp"
#include "include/raylib.hpp"
#include "include/RenderTexture.hpp"
#include "include/Texture.hpp"
using namespace std;
Color shadow = Color{160, 160, 164, 255};

std::vector<std::string> texture_files = {
    "wall.png",
    "baldi-floor.png"
};

bool running = true;
bool inDialog = false;
bool moved = false;

std::vector<Texture2D> textures;
std::vector<Vector2> maps = {
    Vector2{0, -1},
    Vector2{1, 0},
    Vector2{0, 1},
    Vector2{-1, 0}
};

std::string make_lowercase(std::string data) { // stackoverflow my beloved
    std::transform(data.begin(), data.end(), data.begin(),
        [](unsigned char c){ return std::tolower(c); });
    
    return data;
}

// for string delimiter
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
void reroll() { // rerolls the random number generator
    for (int i = 0; i < GetRandomValue(10, 100); i++) {
        GetRandomValue(0, 0xFFFF);
    }
}

std::vector<Vector3> absolute_room_pos;
std::vector<Model> room_models;

float room_size = 4.0f;

std::vector<Vector3> room_offsets = {
    Vector3{0.0f, 0.0f, room_size / 2},
    Vector3{room_size / 2, 0.0f, 0.0f},
    Vector3{0.0f, 0.0f, -room_size / 2},
    Vector3{-room_size / 2, 0.0f, 0.0f}
};

void draw_room(int index, bool map) { // the life of this program is this
    std::vector<int> room = rooms[index]; // get room data

    for (int i = 0; i < room.size(); i++) {
        if (room[i] != 0) { // if there should be a wall there
            Vector3 size;

            if (i % 2 == 0) {
                size = Vector3{room_size, 4.0f, 0.25f}; // determine its size
            } else {
                size = Vector3{0.25f, 4.0f, room_size};
            }

            Mesh mesh = GenMeshCube(size.x, size.y, size.z); // make a mesh
            Model model = LoadModelFromMesh(mesh);
            Vector3 position;

            position.x = room_positions[index][0] * room_size; // position it
            position.z = room_positions[index][1] * room_size;
            position.y = 2;

            position = Vector3Add(position, room_offsets[i]); // add the offset for the wall

            Color clr = room_colors[index];

            if (!map) { // texture it, but only if it's NOT on the minimap
                if (room_wall_textures[index] != -1) {
                    clr = WHITE;

                    model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = textures[room_wall_textures[index]];
                }

                if (i % 2 == 0) {
                    clr = ColorTint(clr, shadow);
                }
            } else {
                clr = WHITE;
            }

            DrawModel(model, position, 1.0f, clr); // draw the wall
        }
    }

    Mesh floorMesh = GenMeshPlane(room_size, room_size, 1, 1);
    Model floorModel = LoadModelFromMesh(floorMesh);
    Vector3 position; // draw the floor
    position.x = room_positions[index][0] * room_size;
    position.z = room_positions[index][1] * room_size;
    position.y = 0;

    Color clr = room_floors[index];
    if (!map) {
        if (room_floor_textures[index] != -1) {
            clr = WHITE;

            floorModel.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = textures[room_floor_textures[index]];
        }
    } else {
        clr = BLACK;
    }

    DrawModel(floorModel, position, 1.0f, clr);
    position.y = 4;

    Model ceilModel = LoadModelFromMesh(floorMesh); // draw the ceiling

    ceilModel.transform = MatrixRotateX(DEG2RAD * 180);

    clr = room_tops[index];

    if (!map) {
        if (room_top_textures[index] != -1) {
            clr = WHITE;

            ceilModel.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = textures[room_top_textures[index]];
        }
    }

    DrawModel(ceilModel, position, 1.0f, clr);

    // it's over
}

std::vector<int> get_croom(Vector2 room_pos) {
    int index = 0;
    for (auto i: room_positions) {
        index += 1;

        if (i[0] == room_pos.x && i[1] == room_pos.y) {
            return rooms[index];
        }
    }

    return {1, 1, 1, 1};
}

bool determine_can_move(Vector3 from, std::vector<int> to) {
    int to_check = -1;

    for (int i = 0; i < maps.size(); i++) {
        if (from.x == maps[i].x && from.z == maps[i].y) {
            to_check = i;
            break;
        }
    }

    if (to_check == -1) {
        return false;
    }

    std::cout << to_check << endl;

    if (!to[to_check] || !to[(to_check + 2) % to.size()]) {
        return true;
    }

    return false;
}

int main() {
    SetRandomSeed(time(NULL));
    SetTraceLogLevel(LOG_ERROR);

    // WINDOW SETTINGS HERE

    int scale = 3;
    const int screen_width = 320;
    const int screen_height = (screen_width / 4) * 3;

    int window_width = screen_width * scale;
    int window_height = screen_height * scale;

    // WINDOW SETTINGS DONE

    InitWindow(window_width, window_height, "Adventure");

    RenderTexture2D target = LoadRenderTexture(screen_width, screen_height);
    RenderTexture2D minimap = LoadRenderTexture(screen_width, screen_height);

    // camera setup code "borrowed" from Raylib docs

    Camera camera = { 0, 0, 0 };
    camera.position = Vector3{ 0.0f, 2.0f, 4.0f };    // Camera position
    camera.target = Vector3{0.0f, camera.position.y, 1.0f};
    camera.up = Vector3{ 0.0f, 1.0f, 0.0f };          // Camera up vector (rotation towards target)
    camera.fovy = 70.0f;                                // Camera field-of-view Y
    camera.projection = CAMERA_PERSPECTIVE;

    Camera mm_cam = { 0, 0, 0 };
    mm_cam.position = Vector3{ 0.0f, 5.0f, 4.0f };    // Camera position
    mm_cam.target = Vector3{0.0f, -8, 0.0f};
    mm_cam.up = Vector3{ 0.0f, 1.0f, 0.0f };          // Camera up vector (rotation towards target)
    mm_cam.fovy = 70.0f;                                // Camera field-of-view Y
    mm_cam.projection = CAMERA_ORTHOGRAPHIC;

    Mesh cubeMesh = GenMeshCube(1.0f, 1.0f, 1.0f);
    Model cube = LoadModelFromMesh(cubeMesh);

    Model marker = LoadModelFromMesh(cubeMesh);

    Mesh sunMesh = GenMeshSphere(8, 8, 8);
    Model sunModel = LoadModelFromMesh(sunMesh);

    bool show_map = false;

    Vector3 direction = Vector3{0.0f, 0.0f, -1.0f * room_size};
    Vector3 camera_angle = Vector3{camera.position.x, camera.position.y, camera.position.z - 1.0f};
    int cam_direction = 0;
    bool shouldMove = false;
    bool justRotate = false;
    bool dontRotate = false;
    Vector3 delta;

    for (auto i: texture_files) {
        Texture2D text = LoadTexture(i.c_str());
        textures.push_back(text);
        std::cout << "Loaded " << i << endl;
    }

    SetTargetFPS(60);
    DisableCursor();

    std::vector<Vector3> deltas = {
        Vector3{0.0f, 0.0f, -room_size},
        Vector3{room_size, 0.0f, 0.0f},
        Vector3{0.0f, 0.0f, room_size},
        Vector3{-room_size, 0.0f, 0.0f}
    };

    InitAudioDevice();

    Music music = LoadMusicStream("music.mp3");
    Sound blip = LoadSound("step.wav");
    Sound bonk = LoadSound("bonk.wav");

    PlayMusicStream(music);
    SetMusicVolume(music, 1.0f);

    while (!WindowShouldClose()) {
        UpdateMusicStream(music);

        cam_direction %= deltas.size();

        if (IsKeyPressed(KEY_M)) {
            show_map = !show_map;
        }

        if (IsKeyPressed(KEY_W)) {
            delta = deltas[cam_direction];
            shouldMove = true;
        }

        if (IsKeyPressed(KEY_A)) {
            cam_direction -= 1;
            cam_direction %= deltas.size();
            delta = deltas[cam_direction];
            shouldMove = true;
            justRotate = true;
        }

        if (IsKeyPressed(KEY_D)) {
            cam_direction += 1;
            cam_direction %= deltas.size();
            delta = deltas[cam_direction];
            shouldMove = true;
            justRotate = true;
        }


        if (shouldMove) {
            Vector3 next_position = Vector3Add(camera.position, delta);
            next_position = Vector3Divide(next_position, Vector3{4, 1, 4});

            Vector2 next_topdown = Vector2{next_position.x, next_position.z};
            Vector3 current_room_vec = Vector3Divide(camera.position, Vector3{4, 1, 4});
            std::vector<int> current_room = get_croom(Vector2{current_room_vec.x, current_room_vec.z});
            bool canMove = false;

            canMove = determine_can_move(Vector3Divide(delta, Vector3{4, 1, 4}), current_room);

            shouldMove = false;
            bool found = false;

            if (!justRotate) {
                for (auto i: room_positions) {
                    if (i[0] == next_topdown.x && i[1] == next_topdown.y and canMove) {
                        camera.position = Vector3Add(camera.position, delta);
                        found = true;
                    }
                }

                if (!found) {
                    PlaySound(bonk);
                }
            };

            if (justRotate) {
                PlaySound(blip);
            }

            justRotate = false;

            if (!dontRotate) {
                camera.position = Vector3Add(camera.position, delta);
                camera_angle = Vector3Add(camera.position, delta);
                camera.position = Vector3Subtract(camera.position, delta);
            }

            dontRotate = false;

            if (found && !justRotate) {
                PlaySound(blip);
            }
        }

        camera.target = camera_angle;
        mm_cam.target.x = camera.target.x;
        mm_cam.target.z = camera.target.z;

        mm_cam.position.x = camera.position.x;
        mm_cam.position.z = camera.position.z;

        BeginTextureMode(target);

        ClearBackground(SKYBLUE);

        BeginMode3D(camera);

        DrawModel(sunModel, Vector3{0, 15, 0}, 1.0f, YELLOW);

        for (int i = 0; i < rooms.size(); i++) {
            draw_room(i, false);
        }

        EndMode3D();

        EndTextureMode();

        BeginTextureMode(minimap);

        ClearBackground(BLACK);

        BeginMode3D(mm_cam);

        ClearBackground(BLACK);

        for (int i = 0; i < rooms.size(); i++) {
            draw_room(i, true);
        }

        Vector3 marker_pos = mm_cam.position;
        marker_pos.y = 2.0f;

        DrawModel(marker, marker_pos, 1.0f, RED);

        EndMode3D();

        EndTextureMode();

        BeginDrawing();

        DrawTexturePro(target.texture, Rectangle{0, 0, screen_width, -screen_height}, Rectangle{0, 0, (float)window_width, (float)window_height}, Vector2{0, 0}, 0.0f, WHITE);

        if (show_map) {
            DrawTexturePro(minimap.texture, Rectangle{0, 0, screen_width, -screen_height}, Rectangle{0, 0, (float)window_width / 2, (float)window_height / 2}, Vector2{0, 0}, 0.0f, WHITE);
        }
        EndDrawing();
    }

    CloseWindow();

    return 0;
}