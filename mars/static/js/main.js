// Notification Fade Out
$(document).ready(function () {
    setTimeout(function () {
        $('.notif-dismiss').addClass('fadeOut');
        setTimeout(function () {
            $('.notif-dismiss').remove();
        }, 1000)
    }, 4000);

    // Add Card Form Reveal
    $('.new_card').css('display', 'none');
    $('#reveal_form').on('click', function (event) {
        $('.new_card').css('display', 'block');
    });

    // Set Fullheight against footer
    var footerHeight = $('.footer').height();
    var res = 100 - footerHeight;
    var height = res + 'vh';
    $('.is-fullheight-menu').css('height', height);
});

// Animate.css Function
$.fn.extend({
    animateCss: function (animationName, callback) {
        var animationEnd = (function (el) {
            var animations = {
                animation: 'animationend',
                OAnimation: 'oAnimationEnd',
                MozAnimation: 'mozAnimationEnd',
                WebkitAnimation: 'webkitAnimationEnd',
            };

            for (var t in animations) {
                if (el.style[t] !== undefined) {
                    return animations[t];
                }
            }
        })(document.createElement('div'));

        this.addClass('animated ' + animationName).one(animationEnd, function () {
            $(this).removeClass('animated ' + animationName);

            if (typeof callback === 'function') callback();
        });

        return this;
    },
});

// Cookie Grabber (Mainly used for CSRF token)
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

// Notifications - Noty lib Handler
var Notify = (function (msg, title, html) {
    var title = title || "Heads up..."
    var text = html || "<p class='subtitle is-5 has-text-light'>" + title + "</p><p>" + msg + "</p>"

    var create = function (type, timeout) {
        var to = timeout || 6000
        return {
            text: text,
            theme: 'metroui',
            type: type,
            layout: 'topRight',
            closeWith: ['click', 'button'],
            timeout: to,
            killer: true,
        }
    }

    var info = function () {
        var note = new Noty(create('info'))
        return note.show()
    }

    var error = function () {
        var note = new Noty(create('error'))
        return note.show()
    }

    return {
        info: info,
        error: error
    }
})

// Handle Ajax
var HandleAjax = (function (el, success, error, action, method, data, type) {
    // Variables and Setup
    var type = type || ''
    var debug;
    var action = action || el.attr('action')
    var method = method || el.attr('method')
    var success = success || function (data) {
        if (debug) {
            console.log('HandleAjax (Success) : ')
            debug = data
            return data
        }
    }
    var error = error || function (data) {
        console.log('HandleAjax (Error) : ')
        debug = data
        return data
    }
    // Serialize form data and append CSRF token
    var data = data || (function () {
        var _data = el.serializeArray();
        _data.push({
            name: 'csrfmiddlewaretoken',
            value: getCookie('csrftoken')
        })
        return _data
    })();
    var request = {
        url: action,
        type: method,
        data: data,
        dataType: type,
        success: success,
        error: error
    }

    // Submit Request
    var submit = function () {
        $.ajax({
            url: el.attr('action'),
            type: el.attr('method'),
            data: data,
            success: success,
            error: error,
        })
    }

    // Publicize
    return {
        debug: debug,
        data: data,
        request: request,
        submit: submit
    };

})

// Cleave Input - Cleave Lib Handling
var LoadCleave = (function (phone, date) {
    // Input Vars
    var phone = phone || {
        selector: $('.js-phone-input'),
        cleave_params: {
            phone: true,
            phoneRegionCode: 'US'
        }
    }

    var date = date || {
        selector: $('.js-date-input'),
        cleave_params: {
            date: true,
            datePattern: ['m', 'y']
        }
    }

    var inputs = $([date, phone])

    // Init
    var init = function () {
        var cleaved_inputs = []
        $(inputs).each(function (pos, input) {
            $(input.selector).each(function (pos, el) {
                var cleave = new Cleave($(el), input.cleave_params)
                cleaved_inputs.push($(el))
            })
        })
        return cleaved_inputs
    }

    return init();
})

// Load needed functions on page  load
$(document).ready(function () {
    // Cleave
    LoadCleave();
})