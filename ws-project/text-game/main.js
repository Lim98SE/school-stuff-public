// document element definition
const GUI_bank = document.getElementById("gui_my_cash")
const GUI_reveal_stocks = document.getElementById("reveal_stocks")
const GUI_stock_container = document.getElementById("stocks")
const GUI_reveal_prices = document.getElementById("reveal_prices")
const GUI_price_container = document.getElementById("prices")
const GUI_stocks = [
    document.getElementById("gui_stock_a"),
    document.getElementById("gui_stock_b"),
    document.getElementById("gui_stock_c"),
    document.getElementById("gui_stock_d")
]

const GUI_main = document.getElementById("game_container")
const GUI_gameover = document.getElementById("gameover_div")
GUI_gameover.hidden = true;

const GUI_prices = [
    document.getElementById("gui_price_a"),
    document.getElementById("gui_price_b"),
    document.getElementById("gui_price_c"),
    document.getElementById("gui_price_d")
]
const GUI_day = document.getElementById("gui_day")
const GUI_graph = document.getElementById("graph")
const ctx = GUI_graph.getContext("2d")

const colors = [
    "#FF0000",
    "#FFFF00",
    "#00FF00",
    "#00FFFF",
]

const logfield = document.getElementById("log")
const player_command = document.getElementById("control")
const command_aliases = [
    ["help", "?"],
    ["sleep", "n"],
    ["sell", "s"],
    ["buy", "b"],
    ["deposit", "d"],
    ["withdraw", "w"],
    ["balance", "l"],
    ["reset", "r"]
]

// player variables
var player_balance = 10000
var day = 1
var stocks = [500, 500, 500, 500]
var stock_trends = [2, 0, -1, 5]
var player_shares = [0, 0, 0, 0]
const stock_names = [
    "$ABCD",
    "$EFGH",
    "$IJKL",
    "$MNOP"
]
var bank_balance = 0;
const bank_interest = 1.05
var stock_history = []
stock_history.concat(stocks)

GUI_stock_container.hidden = true;
GUI_price_container.hidden = true;

// function decloration

const newline = document.createElement("br")

function rerollStocks() {
    for (var i = 0; i < 4; i++) {
        stock_trends[i] = Math.floor(Math.random() * 200) - 100

        if (Math.floor(Math.random() * 10) == 2) {
            stock_trends[i] = Math.floor(Math.random() * 600) - 300

            if (Math.floor(Math.random() * 10) == 2) {
                stock_trends[i] = Math.floor(Math.random() * 2000) - 1000
            }
        }
    }
}

rerollStocks()

function updateUI() {
    GUI_bank.innerText = "$" + player_balance
    
    for (let i = 0; i < 4; i++) {
        GUI_stocks[i].innerText = stock_names[i] + ": " + player_shares[i]
        GUI_prices[i].innerText = stock_names[i] + ": $" + stocks[i]
    }

    GUI_day.innerText = "Day " + day
    drawGraph()
};

function output(text) {
    updateUI()
    var elem = document.createElement("text")
    elem.innerHTML = text
    elem.innerHTML += "<br>"
    logfield.appendChild(elem)
    logfield.scrollTop = logfield.scrollHeight
}

function buy_stock(args) {
    stock_name = args[0]
    var shares = 1
    if (typeof(args[1]) === "undefined") {
        shares = 1
    } else {
        shares = parseInt(args[1])
    }

    if (shares == NaN) {
        shares = 1
    }
    if (stock_name == "all") {
        for (var i = 0; i < 4; i++) {
            buy(i, shares);
        }

        return
    }
    if (!stock_name.includes("$")) {
        stock_name = "$" + stock_name
    }

    if (stock_names.includes(stock_name.toUpperCase())) {
        buy(stock_names.indexOf(stock_name.toUpperCase()), shares)
    } else {
        output("<span class=\"error\">Stock " + stock_name + " doesn't exist.</span>")
    }
}

function buy(stock, shares) {
    if (stocks[stock] * shares > player_balance) {
        output("<span class=\"error\">You can't afford that.</span>")
        return false
    }

    player_balance -= stocks[stock] * shares;
    player_shares[stock] += shares;
    output("You bought " + shares + " shares in <span class=\"stock_" + (stock + 1) + "\">" + stock_names[stock] + "</span>");
    return true
}

function help_command(args) {
    output("STOCK GAME HELP")
    output("buy / b -> buy stocks (example: buy abcd 5 to buy 5 shares in $ABCD)")
    output("sell / s -> sell stocks (example: sell abcd 5 to sell 5 shars in $ABCD")
    output("for BUY and SELL you can use \"all\" to buy/sell all stocks (example: buy all 3)")
    output("deposit / d -> deposit into the bank (example: deposit 5000 to deposit $5000 into the bank)")
    output("balance / l -> see bank balance")
    output("withdraw / w -> withdraw from the bank (example: withdraw all to withdraw everything from the bank)")
    output("the bank gains 5% interest every day")
    output("sleep / n -> go to the next day to see how stocks change & increase money in bank")
    output("try to buy low and sell high. deposit any extra money into the bank, but keep a cushion!")
    output("reset /r -> reset the game")
}

function sell_cmd(args) {
    var shares = 1

    if (typeof(args[1]) === "undefined") {
        shares = 1
    } else {
        shares = parseInt(args[1])
    }

    let stock_name = args[0]

    if (stock_name == "all") {
        for (var i = 0; i < 4; i++) {
            sell(i, shares);
        }

        return
    }
    if (!stock_name.includes("$")) {
        stock_name = "$" + stock_name
    }
    if (stock_names.includes(stock_name.toUpperCase())) {
        stock = stock_names.indexOf(stock_name.toUpperCase())
    } else {
        output("<span class=\"error\">Stock " + stock_name + " doesn't exist.</span>")
        return false
    }

    sell(stock, shares)
}

function sell(stock, shares) {

    if (shares == NaN) {
        shares = 1
    }

    if (shares > player_shares[stock]) {
        output("<span class=\"error\">You can't sell stocks you don't own.</span>")
        return false
    }
    player_balance += stocks[stock] * shares;
    player_shares[stock] -= shares;
    output("You sold " + shares + " shares in <span class=\"stock_" + (stock + 1) + "\">" + stock_names[stock] + "</span>");
    return true
}

const commands = [
    help_command,
    next_day,
    sell_cmd,
    buy_stock,
    deposit,
    withdraw,
    check_bank,
    startGame
]

function runCommand() {
    var raw = player_command.value
    var args = raw.split(" ")
    var command = raw.split(" ")[0]

    if (args.length > 1) {
        args.shift()
    }

    player_command.value = ""
    output("> " + raw)
    command = command.toLowerCase()

    var real_command = -1;

    for (const element of command_aliases) {
        if (element.includes(command)) {
            real_command = command_aliases.indexOf(element);
        }
    }

    if (real_command == -1) {
        output("<span class=\"error\">Error: command not found</span>")
    } else {
        commands[real_command](args)
    }

    updateUI()
}

function startGame() {
    for (const node of logfield.childNodes) {
        node.remove()
    }
    output("Welcome! You are a person trying to become wealthy.<br>You have been loaned $10,000 by your uncle.<br>Your goal is to turn that $10K into $1M in 90 days.<br>Type \"?\" for help, or start buying stocks!")
    updateUI()
}

function toggleStockVisibility() {
    GUI_stock_container.hidden = !GUI_stock_container.hidden
}

function togglePriceVisibility() {
    GUI_price_container.hidden = !GUI_price_container.hidden
}

function deposit(args) {
    let money = parseInt(args[0])
    if (money == NaN) {
        output("<span class=\"error\">Can't deposit NaN dollars.</span>")
        return
    }

    if (money >= player_balance) {
        output("<span class=\"error\">Can't deposit everything you have.</span>")
        return
    }

    bank_balance += money;
    player_balance -= money;
    output("Deposited $" + money + " into the bank.")
}

function withdraw(args) {
    let money = parseInt(args[0])
    if (args[0] == "all") { money = bank_balance }
    if (money == NaN) {
        output("<span class=\"error\">Can't withdraw NaN dollars.</span>")
        return
    }

    if (money > bank_balance) {
        output("<span class=\"error\">Can't withdraw more money than you have.</span>")
        return
    }

    bank_balance -= money;
    player_balance += money;
    output("Withdrew $" + money + " from the bank.")
}

function check_bank(args) {
    output("You have $" + bank_balance + " in the bank.")
}

function next_day(args) {
    output("You went to sleep.")
    day += 1
    if (day == 90) {
        if (player_balance + bank_balance > 1000000) {
            output("Congratualtions! You win!")
        }
        else {
            output("you suck lmaoooo")
        }
    }
    let current_bank = bank_balance
    bank_balance *= bank_interest
    bank_balance = Math.floor(bank_balance)
    if (bank_balance != current_bank) {
        output("Bank balance gained interest: " + current_bank + " -> " + bank_balance)
    }

    for (var i = 0; i < 4; i++) {
        var original = stocks[i]
        stocks[i] += stock_trends[i]
        if (stocks[i] <= 0) {
            stocks[i] = 1
        }

        var delta = stocks[i] - original

        if (original > stocks[i]) {
            output("<span class=\"stock_" + (i + 1) + "\">" + stock_names[i] + "</span> went down by $" + Math.abs(delta))
            continue
        }

        if (original < stocks[i]) {
            output("<span class=\"stock_" + (i + 1) + "\">" + stock_names[i] + "</span> went up by $" + Math.abs(delta))
            continue
        }

        output("<span class=\"stock_" + (i + 1) + "\">" + stock_names[i] + "</span> stayed the same.")
    }

    let current_stocks = JSON.parse(JSON.stringify(stocks));
    stock_history = stock_history.concat(current_stocks)

    rerollStocks()
}

function max(args) {
    let c = -Infinity
    for (const elem of args) {
        if (elem > c) { c = elem }
    }
    return c
}

function drawGraph() {
    ctx.fillRect(0, 0, GUI_graph.width, GUI_graph.height)
    ctx.lineWidth = 3
    ctx.stokeStyle = "#222";
    var step = 1000 / 90

    for (var line = 0; line < 1000; line += 100) {
        ctx.strokeStyle = "#222";
        ctx.beginPath()
        ctx.moveTo(0, line)
        ctx.lineTo(1000, line)
        ctx.stroke()
    }

    for (var line = 0; line < 90; line++) {
        ctx.strokeStyle = "#222";
        ctx.beginPath()
        ctx.moveTo(line * step, 0)
        ctx.lineTo(line * step, 1000)
        ctx.stroke()
    }

    for (var g_day = 0; g_day < stock_history.length; g_day += 4) {
        let current_stock_day = Math.floor(g_day / 4)
        let current_day_stocks = stock_history.slice(g_day, g_day + 4);
        let previous_day_stocks = current_day_stocks
        if (g_day > 0) {
            previous_day_stocks = stock_history.slice(g_day - 4, g_day);
        } else {
            previous_day_stocks = current_day_stocks
        }

        for (var line = 0; line < 4; line++) {
            if (line == 0) {ctx.strokeStyle = "#F00"}
            if (line == 1) {ctx.strokeStyle = "#FF0"}
            if (line == 2) {ctx.strokeStyle = "#0F0"}
            if (line == 3) {ctx.strokeStyle = "#0FF"}
            ctx.beginPath()
            ctx.moveTo((current_stock_day) * step, 1000 - previous_day_stocks[line])
            ctx.lineTo((current_stock_day + 1) * step, 1000 - current_day_stocks[line])
            ctx.stroke()
        }
    }

    ctx.stroke()
}

function gameover() {
    let scores_req = fetch("get_scores.php").then((response) => response.json()).then((json) => sort(json));
    GUI_main.hidden = true;
    GUI_gameover.hidden = false;
}

function sort(scores) {
    scores.sort(sort_array)
    scores.reverse();

    const div = document.getElementById("leaderboard")

    for (let i = 0; i < Math.min(scores.length, 3); i++) {
        // let elem = document.createElement("p");
        // elem.innerText = "#" + (i + 1) + " - " + scores[i].name + " got " + scores[i].score;
        // div.appendChild(elem);
        output("#" + (i + 1) + " - " + scores[i].name + " got " + scores[i].score)
    }
}

function sort_array(a, b) {
    asc = parseInt(a.score)
    bsc = parseInt(b.score)
    if (asc > bsc) { return 1 }
    if (asc < bsc) { return -1 }
    return 0
}

player_command.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      runCommand()
    }
  }); 

window.onload = startGame