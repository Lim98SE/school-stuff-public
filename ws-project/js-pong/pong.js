const screen = document.getElementById("screen")
const context = screen.getContext("2d")
const root = document.getElementById("root")
const dbgToggle = document.getElementById("dbg_toggle")
const monitor = document.getElementById("monitor")

const SND_hit = new Audio("sfx/hit.wav")
const SND_player_score = new Audio("sfx/playerScore.wav")
const SND_com_score = new Audio("sfx/comScore.wav")

dbgToggle.hidden = true

let tick = 0
let pauseTicks = 0
let gameState = 2
// 0 -> ingame
// 1 -> waiting for start
// 2 -> waiting for power-on

var mousePos = {
    x: 0,
    y: 0
}

var ballPos = {
    x: 800 / 2,
    y: 600 / 2
}

var ballVelocity = {
    x: 5,
    y: 0
}

var bgPos = {
    x: 0,
    y: 0
}

var bgVelocity = {
    x: 0,
    y: 0
}

let comPaddle = 0
let player_score = 0
let com_score = 0
let com_speed = 0.05

// thanks, https://stackoverflow.com/questions/17130395/real-mouse-position-in-canvas

function get_mouse_pos(scr, event) {
    var rect = scr.getBoundingClientRect()

    mousePos = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

function score() {
    if (ballPos.x < screen.width / 2) { // scored on p1
        player_score++
        SND_com_score.play()
    } else {
        com_score++
        if (com_speed < 0.5) {
            com_speed += 0.01
        }
        SND_player_score.play()
    }

    pauseTicks = 60
    ballPos = {
        x: 800 / 2,
        y: 600 / 2
    }

    ballVelocity = {
        x: Math.random() > 0.5 ? 5 : -5,
        y: 0
    }
}

function moveBall() {
    ballPos.x += ballVelocity.x
    ballPos.y += ballVelocity.y

    if (ballPos.x < 0 | ballPos.x > screen.width - 16) {
        score()
    }

    if (ballPos.y < 0 | ballPos.y > screen.height - 16) {
        ballVelocity.y *= -1
        SND_hit.play()

        if (ballPos.y < 0) { ballPos.y = 0 }
        if (ballPos.y > screen.height - 16) { ballPos.y = screen.height - 16 }
    }
}

function checkBallCollision() {
    if (ballPos.x < 16) { // ball is in player's side of the court
        if (ballPos.y <= mousePos.y + 96 & ballPos.y + 16 >= mousePos.y) {
            ballVelocity.x *= -1
            ballPos.x = 16

            let centerMouse = mousePos.y + 48
            let centerBall = ballPos.y + 8

            let delta = centerBall - centerMouse
            ballVelocity.y = delta / 8
            SND_hit.play()
        }
    } else if (ballPos.x > screen.width - 32) { // ball is in com's side of the court
        if (ballPos.y <= comPaddle + 96 & ballPos.y >= comPaddle) {
            ballVelocity.x *= -1
            ballPos.x = screen.width - 32

            let centerMouse = comPaddle + 48
            let centerBall = ballPos.y + 8

            let delta = centerBall - centerMouse
            ballVelocity.y = delta / 8
            SND_hit.play()
        }
    }
}

// thanks the medium
function lerp( a, b, alpha ) {
    return a + alpha * ( b - a)
}

function moveCom() {
    comPaddle = lerp(comPaddle, ballPos.y - 48, com_speed)
}

context.font = "64px monospace"

function updateScreen() {
    context.fillStyle = "rgba(0, 0, 0, 0.1)"
    context.clearRect(0, 0, screen.width, screen.height)

    context.fillStyle = "#FFF"

    for (let i = 0; i < 100; i++) {
        context.fillRect((screen.width / 2) - 2, i * 8, 4, 4)
    }

    context.fillText(com_score, (screen.width / 2) - 16 - 128, 64)
    context.fillText(player_score, (screen.width / 2) - 16 + 128, 64)

    context.fillStyle = "#FFF"
    context.fillRect(8, mousePos.y, 8, 96)
    context.fillRect(ballPos.x, ballPos.y, 16, 16)
    context.fillRect(screen.width - 16, comPaddle, 8, 96)
}

function startGame() {
    if (gameState == 1) {
        gameState = 0
        pauseTicks = 60
        player_score = 0
        com_score = 0
    }
}

var moveBg = true;
var damping = 4

function tickGame() {
    tick += 1
    pauseTicks -= 1

    if (moveBg) {
        dbgToggle.innerText = "Disable Dynamic Background"
    } else {
        dbgToggle.innerText = "Enable Dynamic Background"
    }

    if (gameState == 0) {

        bgPos.x += bgVelocity.x / damping
        bgPos.y += bgVelocity.y / damping

        if (moveBg) {
            bgVelocity.x = lerp(ballVelocity.x, bgVelocity.x, 0.95)
            bgVelocity.y = lerp(ballVelocity.y, bgVelocity.y, 0.95)
        } else {
            bgVelocity.x = lerp(bgVelocity.x, 0, 0.05)
            bgVelocity.y = lerp(bgVelocity.y, 0, 0.05)
        }

        root.style.backgroundPositionX = bgPos.x + "px"
        root.style.backgroundPositionY = bgPos.y + "px"

        if (pauseTicks > 0) { moveCom(); updateScreen(); return }

        moveBall()
        moveCom()
        checkBallCollision()
        updateScreen()

    } else if (gameState == 1) {
        context.fillStyle = "#000"
        context.clearRect(0, 0, screen.width, screen.height)
        context.fillStyle = "#FFF"
        context.fillText("PONG", 24, 64)
        context.fillText("press a key to start", 24, screen.height - 32)
    }
}

onmousemove = (event) => {
    get_mouse_pos(screen, event)
}

function powerOn() {
    if (gameState == 2) {
        gameState = 1
        onkeydown = (event) => { startGame() }
        dbgToggle.hidden = false;
        monitor.style.backgroundColor = "#ffdfb300"
        document.getElementById("power_button").style.backgroundColor = "#FF000000"
        document.getElementById("power_button").style.borderBottom = "none"
        document.getElementById("power_button").style.color = "#00000000"
        screen.style.backgroundColor = "#00000010"
    }
}

setInterval(tickGame, 1 / 60)