
$(document).ready(function(){

    
    $("#query").autocomplete({
    source: '/query_help'
    });

    $('#lucky_bt').click(function(){
        $('#joke').append("<h1 class='lucky'>手气?不存在的.</h1>")
    });

});