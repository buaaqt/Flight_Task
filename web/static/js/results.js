$(document).ready(function(){

    $('.snippet > h3').on("mouseover mouseout",function(event){
        if(event.type == "mouseover"){
            var preview_url = $(this).find('a').attr("href");
            preview_url = preview_url.replace('news','preview');
            $.ajax({
                type: "GET",
                url: preview_url,
                async: false,
                success: function(data){
                    $('#preview').append("<h2>" + data.topic + "</h2>");
                    $('#preview').append("<p class='newsInfo'><span class='newsDate'>" + data.date + "</span><br><span class='newsSrc'>来源:" + data.src + "</span></p>");
                    $('#preview').append("<div class='line'></div><div><p>" + data.content + "</p></div>");
                },
               error:function(data){
                    alert('error');
                }
            });
        }
        else if(event.type == "mouseout"){
            $('#preview').empty(); 
        }
    });
    
});