function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggle_album_star(e) {
    e.preventDefault();
    var parts = window.location.pathname.split('/');
    var album_id = parts[parts.length - 1];
    var url = "/albums/star/"+album_id;
    $.post(url, function(data){
        if (data["success"]) {
            var icon_node = $("#star-album-"+album_id+" i");
            if (data["action"] == "saved"){
                icon_node.removeClass("fa-star-o").addClass("fa-star");
            } else {
                icon_node.removeClass("fa-star").addClass("fa-star-o");
            }
        }
         
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var csrftoken = getCookie('csrftoken');

$().ready(function(){
    $('.star-album').click(toggle_album_star);
})