var g_drawing_buffer = [];
var g_selected_pallet;
var g_led_req_params; // Array [16][32]
var g_last_update = Date.now();
var g_saved_stamp_params;
var g_is_bold_pen_thickness = false;
const g_icon_path = "static/assets/icon/";
const PALLETS = {
    pallet0: { id:"red", color: "red", led: "FF0000" },
    pallet1: { id:"orange", color: "orange", led: "FF4400" },
    pallet2: { id:"yellow", color: "yellow", led: "FF8800" },
    pallet3: { id:"green", color: "green", led: "00FF00" },
    pallet4: { id:"blue", color: "blue", led: "0000FF" },
    pallet5: { id:"violet", color: "violet", led: "FF00FF" },
    pallet6: { id:"pink", color: "pink", led: "FF0088" },
    pallet7: { id:"lightgreen", color: "lightgreen", led: "FFFF00" },
    pallet8: { id:"aqua", color: "aqua", led: "00FFFF" },
    pallet9: { id:"white", color: "white", led: "FFFFFF" },
    pallet10: { id:"eraser", color: "#88888855", led: "000000" },
    pallet11: { id:"trash", color: "#88888855", led: "000000" },
};
var EFFECTS = {
    effect0:{frag:false,off: g_icon_path+"perapera_off.png",on: g_icon_path+"perapera_on.png",filter: "filter-wave"},
    effect1:{frag:false,off: g_icon_path+"jump_off.png",on: g_icon_path+"jump_on.png",filter:"filter-jump"},
    effect2:{frag:false,off: g_icon_path+"explosion_off.png",on: g_icon_path+"explosion_on.png",filter:"filter-explosion"},
    effect3:{frag:false,off: g_icon_path+"exile_off.png",on: g_icon_path+"exile_on.png",filter:"filter-exile"},
    effect4:{frag:false,off: g_icon_path+"rain_off.png",on: g_icon_path+"rain_on.png",filter:"filter-bk-rains"},
};
var STAMPS = {
    stamp0:{ off: g_icon_path+"clownfish_off.png",press: g_icon_path+"clownfish_press.png", url:"static/stamps/clownfish.json" },
    stamp1:{ off: g_icon_path+"rocket_off.png",press: g_icon_path+"rocket_press.png", url:"static/stamps/rocket.json" },
    stamp2:{ off: g_icon_path+"chicken_off.png",press: g_icon_path+"chicken_press.png", url:"static/stamps/chicken.json" },
    stamp3:{ off: g_icon_path+"note_off.png",press: g_icon_path+"note_press.png", url:"static/stamps/note.json" },
    stamp4:{ off: g_icon_path+"dragonfly_off.png",press: g_icon_path+"dragonfly_press.png", url:"static/stamps/dragonfly.json" },
    stamp5:{ off: g_icon_path+"ladybug_off.png",press: g_icon_path+"ladybug_press.png", url:"static/stamps/ladybug.json" },
    stamp6:{ off: g_icon_path+"heart_off.png",press: g_icon_path+"heart_press.png", url:"static/stamps/heart.json" },
    stamp7:{ off: g_icon_path+"chinanago_off.png",press: g_icon_path+"chinanago_press.png", url:"static/stamps/chinanago.json" },
    stamp8:{ off: g_icon_path+"flamingo_off.png",press: g_icon_path+"flamingo_press.png", url:"static/stamps/flamingo.json" },
    stamp9:{ off: g_icon_path+"penguin_off.png",press: g_icon_path+"penguin_press.png", url:"static/stamps/penguin.json" },
}
const CELL_WIDTH = 18;
const CELL_HEIGHT = 18;

const is_mobile_dvice = () => {
    return  /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

const get_touch_event_key = () => {
    return is_mobile_dvice() ? "touchstart" : "click";
}
const updatePallet = () =>{

    for(let id in PALLETS){
        const type = id === g_selected_pallet? "on" : "off";
        const color_path = g_icon_path + PALLETS[id]['id'] + '_' + type + '.png';
        $("#" + id).children('img').attr("src", color_path);
        if(type === "on"){
            const pen_type = g_is_bold_pen_thickness? "_L" : "";
            const pen_opposite_type = g_is_bold_pen_thickness? "" : "_L";
            var pen_path = g_icon_path + 'pen' + '_' + PALLETS[id]['id'] + pen_type +'.png';
            var pen_opposite_path = ''

            if(PALLETS[id]['id'] === 'eraser'){
                pen_path = g_icon_path + 'eraser_on.png';
                pen_opposite_path = g_icon_path + 'eraser_off.png';
            }
            else{
                pen_opposite_path = g_icon_path + 'pen' + '_off' + pen_opposite_type + '.png';
            }

            // change pen color
            if(g_is_bold_pen_thickness === false){
                $("#pen_thin").children('img').attr('src', pen_path);
                $("#pen_bold").children('img').attr('src', pen_opposite_path);
            }
            else{
                $("#pen_bold").children('img').attr('src',  pen_path);
                $("#pen_thin").children('img').attr('src', pen_opposite_path);

            }
        }
    }
}

const setPallet = pallet => {
    g_selected_pallet = pallet;
    updatePallet();
}
const setEffect = effect => {
    let selected_effect = effect;
    for(let id in EFFECTS){
        if(id == selected_effect){
            EFFECTS[id].frag = !EFFECTS[id].frag;
            const type = EFFECTS[id].frag === true? "on" : "off";
            $("#" + id).children('img').attr("src",EFFECTS[id][type]);
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
}

const isInRangeOfCanvas = (x, y) =>{
    if(x<0 || x>=16){
        return false;
    }
    if(y<0 || y>=32){
        return false;
    }
    return true;
}

const setCell = (x, y, pallet) => {
    if(!isInRangeOfCanvas(x, y)){
        return
    }
    const id = "#cell_" + x + "_" + y;
    $(id).css("background-color", PALLETS[pallet].color);
    g_drawing_buffer.push({ 'x' : x, 'y': y, 'color': PALLETS[pallet].led })
    g_led_req_params[x][y] = PALLETS[pallet].led;
}

const setCellFromColorCode = (x, y, colorCode) =>{
    if(!isInRangeOfCanvas(x, y)){
        return
    }
    g_led_req_params[x][y] = colorCode;
    g_drawing_buffer.push({ 'x' : x, 'y': y, 'color': g_led_req_params[x][y] })
    const id = "#cell_" + x + "_" + y;
    if(colorCode == "000000"){
        colorCode = "transparent";
    }
    $(id).css("background-color", colorCode);
}
const updateCellColor = event => {
    var coordinate = getCellCoordinate(event);
    const x = coordinate.x;
    const y = coordinate.y;
    setCell(x, y, g_selected_pallet);
}
const updateCellColorBold = event => {
    var coordinate = getCellCoordinate(event);
    const x = coordinate.x;
    const y = coordinate.y;
    setCell(x, y, g_selected_pallet);
    setCell(x-1, y, g_selected_pallet);
    setCell(x+1, y, g_selected_pallet);
    setCell(x, y-1, g_selected_pallet);
    setCell(x, y+1, g_selected_pallet);
}
const getCellCoordinate = event => {
    const p0 = $("#cells").offset();
    let p1 = undefined;
    if(is_mobile_dvice()){
        p1 = event.changedTouches[0];
    } else {
        p1 = event;
    }
    const x = Math.floor((p1.pageX - p0.left) / (CELL_WIDTH + 3.6));
    const y = Math.floor((p1.pageY - p0.top) / (CELL_HEIGHT + 3.6));
    var coordinate = {x: x,y: y};
    return coordinate;
}
const clearCells = () => {
    for(let x = 0; x < g_led_req_params.length; ++x){
        for(let y = 0; y < g_led_req_params[x].length; ++y){
            setCell(x, y, "pallet11");
        }
    }
//    postCells()
}

const postCell = () =>{

    if (g_drawing_buffer.length == 0){
        return;
    }

    var buffer = []
    for(var i = 0; i<g_drawing_buffer.length; i++){
        buffer.push(g_drawing_buffer[i])
    }
    g_drawing_buffer = []
    $.ajax({
        url:'./api/led',
        type:'POST',
        contentType:'application/json',
        data:JSON.stringify({ points : buffer})
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
        contentType:'application/json',
        data:JSON.stringify({ 'led' : g_led_req_params })
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
    const img_bold = $("<img>").attr("border", 0).attr("src", g_icon_path+"pen_off_L.png").attr("width", "50px").attr("height", "50px");
    const img_thin = $("<img>").attr("border", 0).attr("src", g_icon_path+"pen_red.png").attr("width", "50px").attr("height", "50px");
    $("#pen_thin").on(get_touch_event_key(),event =>{ 
        g_is_bold_pen_thickness=false;
        updatePallet();
    }).append(img_thin);
    
    $("#pen_bold").on(get_touch_event_key(),event => {
        g_is_bold_pen_thickness=true;
        updatePallet();
    }).append(img_bold);
}
function clearEffects() {
    for(let id in EFFECTS){
        EFFECTS[id].frag = false;
        $("#" + id).children('img').attr("src",EFFECTS[id].off);
    }
    postEffect();
}
function pressStamp(id) {
    $("#" + id).children('img').attr("src",STAMPS[id].press);
}
function endPressStamp(id){
    $("#" + id).children('img').attr("src",STAMPS[id].off);
}
function pressTrash(id){
    $("#" + id).children('img').attr("src",g_icon_path + 'trash_on.png');
}
function endPressTrash(id){
    $("#" + id).children('img').attr("src",g_icon_path + 'trash_off.png');
}
$(document).ready(() => {
    disableScroll();
    $("#header").append(
        $("<img>").attr("border", 0).attr("src","static/assets/header/Draw_to_Like_Header.png")
        .attr("width", "768px").attr("height", "96px"));
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
    for(let id in PALLETS){
        const obj = $("#" + id);
        obj.addClass("pallet");
        if(id === "pallet11"){
            const img = $("<img>").attr("border", 0).attr("src", "static/assets/trash.png").attr("width", "62.5px").attr("height", "62.5px");
            obj.on(get_touch_event_key(),event => {clearCells(),clearEffects(),pressTrash(id)}).
            on("touchend",event => endPressTrash(id)).append(img);
        } else {
            const img = $("<img>").attr("border", 0).attr("src", "static/assets/eraser.png").attr("width", "62.5px").attr("height", "62.5px");
            obj.on(get_touch_event_key(), event => setPallet(id)).on("touchmove", event => setPallet(id)).append(img);
        }
    }
    for(let id in EFFECTS){
        const obj = $("#" + id);
        const off = EFFECTS[id].off;
        const img = $("<img>").attr("border", 0).attr("src", off).attr("width", "128px").attr("height", "104px");
        obj.addClass("effect").on(get_touch_event_key(), event => setEffect(id)).append(img);
    }
    for(let id in STAMPS){
        const obj =$("#" + id);
        const off = STAMPS[id].off;
        const img = $("<img>").attr("border", 0).attr("src", off).attr("width", "66px").attr("height", "66px");
        obj.addClass("stamp").on(get_touch_event_key(),event => {setStamp(id),pressStamp(id)}).
        on("touchend",event => endPressStamp(id)).append(img);
    }
    setPallet("pallet0");
    updateWindow();
    $(window).resize(() => {
        updateWindow();
    });

    setInterval(postCells, 10000); // update all
    setInterval(postCell, 100); // send pixels if updates exists.
});