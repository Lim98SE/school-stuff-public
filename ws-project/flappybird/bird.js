const main_screen = document.getElementById("main_gamescreen")
const score_elem = document.getElementById("score")

document.getElementById("gameover").hidden = true

let bird_y = 5;
let bird_vel = 0;
let gravity = 0.2;

let pipes_x = [4, 8, 12, 16, 20]
let pipes_y = [5, 5, 5, 5, 5]

let pipe_advance_frames = 3
let score = 0

let pipe_count = pipes_x.length;

let screen_height = 10;
let screen_width = 20;

function clearScreen() {
    main_screen.innerHTML = "";

    for (let y = 0; y < screen_height; y++) {
        for (let x = 0; x < screen_width; x++) {
            let e = document.createElement("span")
            e.id = x + "/" + y;
            e.innerText = "##";
            e.classList.add("screen_off")
            main_screen.appendChild(e);
        }
        main_screen.appendChild(document.createElement("br"))
    }
}

function drawBird() {
    try {
        let bird_elem = document.getElementById("0/" + bird_y);
        bird_elem.className = "screen_red"
        bird_elem.innerText = "O>"
    } catch {
        checkCollision();
    }
}

function drawPipes() {
    for (let i = 0; i < pipe_count; i++) {
        let x = pipes_x[i];
        let top = pipes_y[i] - 1;
        let bottom = pipes_y[i] + 1;

        try {
            for (let y = 0; y < top; y++) {
                let elem = document.getElementById(x + "/" + y).className = "screen_green";
            }
    
            for (let y = bottom + 1; y < screen_height; y++) {
                let elem = document.getElementById(x + "/" + y).className = "screen_green";
            }
        } catch {
            console.log(";3")
        }
    }
}

function checkCollision() {
    if (bird_y < 0 | bird_y > screen_height) { return -1 }
    for (let i = 0; i < pipe_count; i++) {
        if (pipes_x[i] != 0) { continue; }
        let top = pipes_y[i] - 1;
        let bottom = pipes_y[i] + 1;
        if (bird_y < top | bird_y > bottom) { return -1 }
        score++
        return 0
    }

    return 1
}

function newFrame() {
    bird_y += bird_vel;
    bird_y = Math.floor(bird_y);
    bird_vel += gravity;
    clearScreen();
    drawBird();
    drawPipes();

    pipe_advance_frames -= 1;

    if (pipe_advance_frames == 0) {
        let died = checkCollision();
        if (died == -1) {
            document.getElementById("main").remove();
            document.getElementById("score_go").innerText = score
            document.getElementById("gameover").hidden = false
            document.getElementById("jumpscare").play()
        }
        pipe_advance_frames = 3;
        for (let i = 0; i < pipe_count; i++) {
            pipes_x[i] -= 1;

            if (pipes_x[i] <= -1) {
                pipes_x[i] = screen_width + 1
                pipes_y[i] = Math.floor(Math.random() * (screen_height - 1)) + 1
            }
        }
    }

    score_elem.innerText = score
}

var hasGameStarted = false;

function flap() {
    if (!hasGameStarted) {
        hasGameStarted = true;
        startGame();
        return;
    }
    bird_vel = -0.3;
}

function startGame() {
    for (let i = 0; i < pipe_count; i++) {
        pipes_y[i] = Math.floor(Math.random() * (screen_height - 1)) + 1
    }
    setInterval(newFrame, 100)
}

clearScreen();