// using jQuery
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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).on('submit', '#ajax_form', function (e) {
    e.preventDefault();
    var data = new FormData($('form').get(0));
    $('#ajax_form').find("span.text-danger").html("");
    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data, textStatus, jqXHR) {
            if (data.errors === true) {
                var errors = data.data;
                Object.keys(errors).forEach(function (key) {
                    var selector = "input[name=" + key + "] + span.text-danger"
                    $('#ajax_form').find(selector).html(errors[key])
                })
            } else if (data.errors === false) {
                $(".label-wrapper").css("width", "0");
                $('#ajax_form').trigger("reset");
            }
        },
        error: function (data) {
        },
    });
    return false;
});

$(document).on('submit', '.ajax_comment', function (e) {
    e.preventDefault();
    var data = new FormData($(this).get(0));
    $('#ajax_form').find("span.text-danger").html("");
    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: data, //$(this).serialize(),
        cache: false,
        contentType: false,
        processData: false,
        success: function (data, textStatus, jqXHR) {
            if (data.errors === true) {
                var errors = data.data;
                Object.keys(errors).forEach(function (key) {
                    var selector = "input[name=" + key + "] + span.text-danger";
                    $('#ajax_form').find(selector).html(errors[key])
                })
            } else if (data.errors === false) {
                var form = $(e.target)
                form.trigger('reset');
                form.hide();
                form.parent().parent().find(".add-button").show();
            }
        },
        error: function (data) {
        },
    });
    return false;
});

