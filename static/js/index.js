var g_selected_pallet;
var g_led_req_params; // Array [16][32]
var g_last_update = Date.now();
const PALLETS = {
    pallet0: { color: "transparent", off: "black", on: "red", led: "000000" },
    pallet1: { color: "white", off: "black", on: "red", led: "FFFFFF" },
    pallet2: { color: "red", off: "black", on: "blue", led: "FF0000" },
    pallet3: { color: "yellow", off: "black", on: "red", led: "FF8800" },
    pallet4: { color: "lightgreen", off: "black", on: "red", led: "00FF00" },
    pallet5: { color: "aqua", off: "black", on: "red", led: "00FFFF" },
    pallet6: { color: "blue", off: "black", on: "red", led: "0000FF" },
    pallet9: { color: "pink", off: "black", on: "red", led: "FF0088" },
    pallet10: { color: "violet", off: "black", on: "red", led: "FF00FF" },
    pallet11: { color: "orange", off: "black", on: "blue", led: "FF4400" },
};
const CELL_WIDTH = 16;
const CELL_HEIGHT = 16;

const setPallet = pallet => {
    g_selected_pallet = pallet;
    for(let id in PALLETS){
        const type = id === g_selected_pallet? "on" : "off";
        $("#" + id).css("border-color", PALLETS[id][type]);
    }
}
const updateWindow = () => {
    $(".cell").css("width", CELL_WIDTH).css("height", CELL_HEIGHT);
    const top = ($(window).height() - $("#main").height()) / 2;
    const left = ($(window).width() - $("#main").width()) / 2;
    $("#main").css("margin-top", top).css("margin-left", left);
}
const setCell = (x, y, pallet) => {
    const id = "#cell_" + x + "_" + y;
    $(id).css("background-color", PALLETS[pallet].color);
    g_led_req_params[x][y] = PALLETS[pallet].led;
}
const updateCellColor = event => {
    const p0 = $("#cells").offset();
    const p1 = event.changedTouches[0];
    const x = Math.floor((p1.pageX - p0.left) / (CELL_WIDTH + 3.6));
    const y = Math.floor((p1.pageY - p0.top) / (CELL_HEIGHT + 3.6));
    setCell(x, y, g_selected_pallet);
    postCell(x, y)
}
const clearCells = () => {
    for(let x = 0; x < g_led_req_params.length; ++x){
        for(let y = 0; y < g_led_req_params[x].length; ++y){
            setCell(x, y, "pallet0");
        }
    }
    postCells()
}

const postCell = (x, y) =>{
    $.ajax({
        url:'./api/led',
        type:'POST',
        data:{ 'x' : x, 'y': y, 'color': g_led_req_params[x][y] }
    }).done(data => {}).fail(data => {});
}
const postCells = () => {
    const now = Date.now();
    if(now - g_last_update  < 80){
        return;
    }
    g_last_update = now;
    $.ajax({
        url:'./api/led',
        type:'POST',
        data:{ 'led' : g_led_req_params }
    }).done(data => {}).fail(data => {});
}
$(document).ready(() => {
    $("#cells").on("touchstart", event => {
        updateCellColor(event);
    }).on("touchmove", event => {
        updateCellColor(event);
    });
    updateWindow();
    $(window).resize(() => {
        updateWindow();
    });
    g_led_req_params = new Array(16);
    for(let x = 0; x < g_led_req_params.length; ++x) {
        g_led_req_params[x] = new Array(32).fill(0);
    }
    clearCells();
    $("#trash").click(() => clearCells());
    for(let id in PALLETS){
        const obj = $("#" + id);
        const color = PALLETS[id].color;
        obj.addClass("pallet").on("touchstart", event => setPallet(id)).css("background-color", color)
            .on("touchmove", event => setPallet(id)).css("background-color", color);
        if(color === "transparent"){
            const img = $("<img>").attr("border", 0).attr("src", "static/assets/eraser.png").attr("width", "50px").attr("height", "50px");
            obj.css("background-color", "lightgray").append(img);
        }
    }
    setPallet("pallet0");
//    setInterval(postCells, 100);
});
