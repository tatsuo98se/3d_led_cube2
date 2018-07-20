function update(key, val){
    var json_data = {};
    json_data[key]=val

    $.ajax({
        url:'./api/gamepad',
        type:'POST',
        contentType:'application/json',
        data:JSON.stringify(json_data)
    }).done(data => {}).fail(data => {});


}

$(document).ready(() => {
    /* 変更中（ドラッグ中） */
    $( 'input[type=range]' ).on( 'input', function () {
        update(this.id, this.value/100.0);
    } );

    /* 変更後 */
    $( 'input[type=range]' ).change( function () {
        update(this.id, this.value/100.0);
    } );
});