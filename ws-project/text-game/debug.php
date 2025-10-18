<form method="post" action="submit_score.php">
    <input name="name">
    <input type="hidden" value="500" name="score">
    <button>submit</button>
</form>
<div id="leaderboard">
</div>
<script>
let scores_req = fetch("get_scores.php").then((response) => response.json()).then((json) => sort(json));

function sort(scores) {
    scores.sort(sort_array)
    scores.reverse();

    const div = document.getElementById("leaderboard")

    for (let i = 0; i < Math.min(scores.length, 3); i++) {
        let elem = document.createElement("p");
        elem.innerText = "#" + (i + 1) + " - " + scores[i].name + " got " + scores[i].score;
        div.appendChild(elem);
    }
}

function sort_array(a, b) {
    console.log(a.score + " " + b.score);
    asc = parseInt(a.score)
    bsc = parseInt(b.score)
    if (asc > bsc) { return 1 }
    if (asc < bsc) { return -1 }
    return 0
}

</script>
