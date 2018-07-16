var g_selected_pallet;
var g_led_req_params; // Array [16][32]
var g_last_update = Date.now();
var g_saved_stamp_params;
var g_is_bold_pen_thickness = false;
const PALLETS = {
    pallet0: { color: "red", off: "black", on: "blue", led: "FF0000" },
    pallet1: { color: "orange", off: "black", on: "blue", led: "FF4400" },
    pallet2: { color: "yellow", off: "black", on: "red", led: "FF8800" },
    pallet3: { color: "green", off: "black", on: "red", led: "00FF00" },
    pallet4: { color: "blue", off: "black", on: "red", led: "0000FF" },
    pallet5: { color: "violet", off: "black", on: "red", led: "FF00FF" },
    pallet6: { color: "pink", off: "black", on: "red", led: "FF0088" },
    pallet7: { color: "lightgreen", off: "black", on: "red", led: "55FF00" },
    pallet8: { color: "aqua", off: "black", on: "red", led: "00FFFF" },
    pallet9: { color: "white", off: "black", on: "red", led: "FFFFFF" },
    pallet10: { color: "transparent", off: "black", on: "red", led: "000000" },
    pallet11: { color: "transparent", off: "black", on: "red", led: "000000" },
};
var EFFECTS = {
    effect0:{color:"white",frag:false,filter:"filter-explosion"},
    effect1:{color:"white",frag:false,filter:"filter-jump"},
    effect2:{color:"white",frag:false,filter:"filter-exile"},
    effect3:{color:"white",frag:false,filter:"filter-wave"},
    effect4:{color:"white",frag:false,filter:"filter-bk-rains"},
};
var STAMPS = {
    stamp0:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/chicken.json" },
    stamp1:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/chinanago.json" },
    stamp2:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/clownfish.json" },
    stamp3:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/dragonfly.json" },
    stamp4:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/flamingo.json" },
    stamp5:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/heart.json" },
    stamp6:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/ladybug.json" },
    stamp7:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/note.json" },
    stamp8:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/penguin.json" },
    stamp9:{ color: "pink", off: "black", on: "red", led: "000000", url:"static/stamps/rocket.json" },
}
const CELL_WIDTH = 18;
const CELL_HEIGHT = 18;

const is_mobile_dvice = () => {
    return  /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

const get_touch_event_key = () => {
    return is_mobile_dvice() ? "touchstart" : "click";
}

const setPallet = pallet => {
    g_selected_pallet = pallet;
    for(let id in PALLETS){
        const type = id === g_selected_pallet? "on" : "off";
        $("#" + id).css("border-color", PALLETS[id][type]);
    }
}
const setEffect = effect => {
    let selected_effect = effect;
    for(let id in EFFECTS){
        if(id == selected_effect){
            EFFECTS[id].frag = !EFFECTS[id].frag;
        }
    }
    postEffect();
}

const setJson = filepath =>{
    var json = $.getJSON(filepath, function(json) {

        led = json["led"]
        for(let x = 0; x < g_led_req_params.length; ++x){
            for(let y = 0; y < g_led_req_params[x].length; ++y){
                pallet = searchPallet("led", led[x][y])
                setCell(x, y, pallet)
            }
        }
        postCells()
    });;
}

const setImage = filepath => {

    var img = document.createElement('img');
    img.src = filepath;
    var canvas = document.createElement('canvas');
    img.onload = function () {
        canvas.width = img.width;
        canvas.height = img.height;
        console.log("w : "+ canvas.width +" h : " + canvas.height);
        var context = canvas.getContext('2d');
        context.drawImage(img, 0, 0 );
        var imageData = context.getImageData(0,0,16,32);
        console.log("iamgeData.length : " + imageData.length);
        for(let x = 0; x < g_led_req_params.length; ++x){
            for(let y = 0; y < g_led_req_params[x].length; ++y){
                var rgb = [
                   imageData.data[(x +y * 16) * 4],
                    imageData.data[(x +y * 16) * 4 + 1],
                    imageData.data[(x +y * 16) * 4 + 2]
                ];
                console.log(rgb);
                var colorCode = convertToColorCodeFromRGB(rgb);
                console.log("(x, y) : ("+x+","+y+")"+"colorCode : " + colorCode);
                setCellFromColorCode(x, y, colorCode);
            }
        }
        postCells()
    }
}

const setStamp = stamp => {
    var stamp_url;
    for(let id in STAMPS){
        if(id == stamp){
            stamp_url = STAMPS[id].url;
        }
    }
    if(stamp_url.endsWith("png")){
        setImage(stamp_url)
    }
    else{
        setJson(stamp_url)
    }
}
function convertToColorCodeFromRGB ( rgb ) {
	return rgb.map( function ( value ) {
		return ( "0" + value.toString( 16 ) ).slice( -2 ) ;
	} ).join( "" ) ;
}

const searchPallet = (key, value) => {
    for(let pallet in PALLETS){
        if(value === PALLETS[pallet][key]){
            return pallet;
        }
    }
    return undefined;
}

const updateWindow = () => {
    $(".cell").css("width", CELL_WIDTH).css("height", CELL_HEIGHT);
    // const top = ($(window).height() - $("#main").height()) / 2;
    // const left = ($(window).width() - $("#main").width()) / 2;
    // $("#main").css("margin-top", top).css("margin-left", left);
    // const left_effects = ($(window).width() - $("#effects").width()) / 2;
    // $("#effects").css("margin-left", left_effects);
}
const setCell = (x, y, pallet) => {
    const id = "#cell_" + x + "_" + y;
    $(id).css("background-color", PALLETS[pallet].color);
    g_led_req_params[x][y] = PALLETS[pallet].led;
}
const setCellFromColorCode = (x, y, colorCode) =>{
    g_led_req_params[x][y] = colorCode;
    const id = "#cell_" + x + "_" + y;
    if(colorCode == "000000"){
        colorCode = "transparent";
    }
    $(id).css("background-color", colorCode);
}
const updateCellColor = event => {
    const p0 = $("#cells").offset();
    let p1 = undefined;
    if(is_mobile_dvice()){
        p1 = event.changedTouches[0];
    }
    else{
        p1 = event;
    }


    const x = Math.floor((p1.pageX - p0.left) / (CELL_WIDTH + 3.6));
    const y = Math.floor((p1.pageY - p0.top) / (CELL_HEIGHT + 3.6));
    setCell(x, y, g_selected_pallet);
    postCell(x, y)
}
const updateCellColorBold = event => {
    const p0 = $("#cells").offset();
    let p1 = undefined;
    if(is_mobile_dvice()){
        p1 = event.changedTouches[0];
    }
    else{
        p1 = event;
    }


    const x = Math.floor((p1.pageX - p0.left) / (CELL_WIDTH + 3.6));
    const y = Math.floor((p1.pageY - p0.top) / (CELL_HEIGHT + 3.6));
    setCell(x, y, g_selected_pallet);
    setCell(x-1, y, g_selected_pallet);
    setCell(x+1, y, g_selected_pallet);
    setCell(x, y-1, g_selected_pallet);
    setCell(x, y+1, g_selected_pallet);
    postCell();
}
const clearCells = () => {
    for(let x = 0; x < g_led_req_params.length; ++x){
        for(let y = 0; y < g_led_req_params[x].length; ++y){
            setCell(x, y, "pallet11");
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
const postEffect = () =>{
    var obj = [];
    for(let id in EFFECTS){
        if(EFFECTS[id].frag){
            obj.push({'id' : EFFECTS[id].filter},)
        }
    }
    console.log(obj);
    var json_data = {
        'filters' : obj
    };
    console.log(json_data);
    $.ajax({
        url:'./api/filters',
        type:'POST',
        contentType:'application/json',
        data:JSON.stringify(json_data)
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
const savePicture = () =>{
    for(let x = 0; x < g_led_req_params.length; ++x){
        for(let y = 0; y < g_led_req_params[x].length; ++y){
            g_saved_stamp_params[x][y] = g_led_req_params[x][y];
            console.log("x : " + x);
            console.log("y : " + y);
            console.log("color : " + g_saved_stamp_params[x][y]);
        }
    }
    postSavedPicture();
}
const postSavedPicture = () =>{
    var obj = {
        'stamp_params' : g_saved_stamp_params
    }
    console.log(obj);
    $.ajax({
        url:'./api/stamp',
        type:'POST',
        contentType:'application/json',
        data:JSON.stringify(obj)
    }).done(data => {}).fail(data => {});
}

function preventDefault(e){
    e.preventDefault();
}

function disableScroll(){
    document.body.addEventListener('touchmove', preventDefault, { passive: false });
}
function setPenThickness() {
    const img_bold = $("<img>").attr("border", 0).attr("src", "static/assets/trash.png").attr("width", "50px").attr("height", "50px");
    const img_thin = $("<img>").attr("border", 0).attr("src", "static/assets/trash.png").attr("width", "50px").attr("height", "50px");
    $("#pen_thin").on(get_touch_event_key(),event => g_is_bold_pen_thickness=false).append(img_thin);
    $("#pen_bold").on(get_touch_event_key(),event => g_is_bold_pen_thickness=true).append(img_bold);
}
$(document).ready(() => {

    disableScroll();
    $("#cells").on(get_touch_event_key(), event => {
        if(g_is_bold_pen_thickness){
            updateCellColorBold(event);
        } else {
            updateCellColor(event);
        }
    }).on("touchmove", event => {
        if(g_is_bold_pen_thickness){
            updateCellColorBold(event);
        } else {
            updateCellColor(event);
        }
    });
    g_led_req_params = new Array(16);
    g_saved_stamp_params = new Array(16);
    for(let x = 0; x < g_led_req_params.length; ++x) {
        g_led_req_params[x] = new Array(32).fill(0);
        g_saved_stamp_params[x] = new Array(32).fill(0);
    }
    clearCells();
    setPenThickness();
    // $("#pen_thin").on(get_touch_event_key(),event => g_is_bold_pen_thickness=true);
    // $("#pen_bole").on(get_touch_event_key(),event => g_is_bold_pen_thickness=false);
    for(let id in PALLETS){
        const obj = $("#" + id);
        const color = PALLETS[id].color;
        obj.addClass("pallet");
        if(id === "pallet11"){
            const img = $("<img>").attr("border", 0).attr("src", "static/assets/trash.png").attr("width", "50px").attr("height", "50px");
            obj.on(get_touch_event_key(),event => clearCells()).css("background-color", "lightgray").append(img);
        } else {
            const img = $("<img>").attr("border", 0).attr("src", "static/assets/eraser.png").attr("width", "50px").attr("height", "50px");
            obj.on(get_touch_event_key(), event => setPallet(id)).css("background-color", color)
            .on("touchmove", event => setPallet(id)).css("background-color", color).append(img);
        }
    }
    for(let id in EFFECTS){
        const obj = $("#" + id);
        const color = EFFECTS[id].color;
        obj.addClass("effect").on(get_touch_event_key(), event => setEffect(id)).css("background-color", color);
    }
    for(let id in STAMPS){
        const obj =$("#" + id);
        const color = STAMPS[id].color;
        obj.addClass("stamp").on(get_touch_event_key(),event => setStamp(id)).css("background-color", color);
    }
    setPallet("pallet0");
    updateWindow();
    $(window).resize(() => {
        updateWindow();
    });
//    setInterval(postCells, 100);
});