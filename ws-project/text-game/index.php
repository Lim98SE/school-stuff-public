<html>
    <head>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div id="game_container">
            <div id="gui_div">
                <text>You:</text>
                <text id="gui_my_cash">$0</text>
                <text id="reveal_stocks" onclick="toggleStockVisibility()">Shares</text>
                <span id="stocks">
                    <text id="gui_stock_a" class="stock_1">0 $ABCD</text>
                    <text id="gui_stock_b" class="stock_2">0 $EFGH</text>
                    <text id="gui_stock_c" class="stock_3">0 $IJKL</text>
                    <text id="gui_stock_d" class="stock_4">0 $MNOP</text>
                </span>
                <text id="reveal_prices" onclick="togglePriceVisibility()">Prices</text>
                <span id="prices">
                    <text id="gui_price_a" class="stock_1">0 $ABCD</text>
                    <text id="gui_price_b" class="stock_2">0 $EFGH</text>
                    <text id="gui_price_c" class="stock_3">0 $IJKL</text>
                    <text id="gui_price_d" class="stock_4">0 $MNOP</text>
                </span>
                <text id="gui_day">Day 1</text>
            </div>
            <div id="main">
                <div id="map">
                    <canvas id="graph" width="1000" height="1000"></canvas>
                </div>
                <div id="playfield">
                    <div id="log">
        
                    </div>
                    <div id="entry_box">
                        <input id="control">
                        <button id="submit_command" onclick="runCommand()">Go</button>
                    </div>
                </div>
            </div>
        </div>
        <div id="gameover_div">
            <h1>Game over!</h1>
            <p>You earned $<span id="final_money">xyz</span>.</p>
            <p>You could have earned $<span id="final_potential">xyz</span> if you sold at the last minute.</p>
            <p>You took <span id="final_money">xyz</span> days to reach $1,000,000.</p>
            <p>You owned <span id="final_stocks">xyz</span> stocks in total. (You sold</p>
        </div>
    </body>
    <script src="main.js"></script>
</html>