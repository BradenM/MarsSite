// Scroll Function (AnimateScroll Handler)
var ScrollTo = function ($sel) {
    var _scroll = function ($target, $el) {
        var target = $target || $el.attr('ani-scroll')
        $(target).animatescroll({
            scrollSpeed: 1500,
            easing: 'easeInOutSine'
        })
    }

    var init = function () {
        var elements = $('[ani-scroll]')
        elements.on('click', function () {
            _scroll($(this))
        })
    }

    if ($sel) {
        _scroll($sel)
    }

    return {
        init: init
    }
}

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

    var init = function () {
        var notifs = $('div[data-notify]');
        notifs.each(function (pos, el) {
            console.log('Notification Detected')
            $el = $(el)
            var _title = $el.attr('data-notify-title') || title
            var _msg = $el.attr('data-notify-msg') || msg
            text = "<p class='subtitle is-5 has-text-light'>" + _title + "</p><p>" + _msg + "</p>"
            switch ($el.attr('data-notify')) {
                case 'info':
                    info()
                    break;
                case 'error':
                    error()
                    break;
                default:
                    console.log('Notify: Bad Parameters')

            }
        })
    }

    var _create = function (type, timeout) {
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
        var note = new Noty(_create('info'))
        return note.show()
    }

    var error = function () {
        var note = new Noty(_create('error'))
        return note.show()
    }

    return {
        info: info,
        error: error,
        init: init
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

// LoadPushbar - Handler for Pushbar.js
var LoadPushbars = (function () {
    var pushbar = new Pushbar({
        blur: true,
        overlay: true
    })
})()

// Load needed functions on page  load
$(document).ready(function () {
    // AniScroll
    ScrollTo().init();
    // Cleave
    LoadCleave();
    // Detect Notifications
    Notify().init()
})