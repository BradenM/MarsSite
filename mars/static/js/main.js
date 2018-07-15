$(document).ready(function () {
    console.log('Main Script file loaded');
    $('#signup_tab').hide();

    jQuery.fn.extend({
        // Animated Scroll
        aniscroll: function () {
            $(this).animatescroll({
                scrollSpeed: 1500,
                easing: 'easeInOutSine'
            });
        },
        // Hardcoded cause im lazy user tab switching function, will fix later
        switchTab: function () {
            var target = this
            console.log('tab switched');
            if (this.is('#signup_tab')) {
                $('#signup_tab').show();
                $('#login_tab').hide();
                $('#login_tab_button').removeClass('is-active');
                $('#signup_tab_button').addClass('is-active');
            } else {
                $('#signup_tab').hide();
                $('#login_tab').show();
                $('#login_tab_button').addClass('is-active');
                $('#signup_tab_button').removeClass('is-active');
            }
            return (false);
        }

    })
})

// Quick View
function closest(el, selector) {
    var matchesFn;

    // find vendor prefix
    ['matches', 'webkitMatchesSelector', 'mozMatchesSelector', 'msMatchesSelector', 'oMatchesSelector'].some(function (fn) {
        if (typeof document.body[fn] == 'function') {
            matchesFn = fn;
            return true;
        }
        return false;
    });

    var parent;

    // traverse parents
    while (el) {
        parent = el.parentElement;
        if (parent && parent[matchesFn](selector)) {
            return parent;
        }
        el = parent;
    }

    return null;
}

document.addEventListener('DOMContentLoaded', function () {
    // Get all document sliders
    var showQuickview = document.querySelectorAll('[data-show="quickview"]');
    [].forEach.call(showQuickview, function (show) {
        var quickview = document.getElementById(show.dataset['target']);
        if (quickview) {
            // Add event listener to update output when slider value change
            show.addEventListener('click', function (event) {
                quickview.classList.add('is-active');
            });
        }
    });
});

$('.quickview').on("mouseenter", function (event) {
    // Get all document sliders
    var dismissQuickView = document.querySelectorAll('[data-dismiss="quickview"]');
    [].forEach.call(dismissQuickView, function (dismiss) {
        var quickview = closest(dismiss, '.quickview');
        if (quickview) {
            // Add event listener to update output when slider value change
            dismiss.addEventListener('click', function (event) {
                quickview.classList.remove('is-active');
            });
        }
    });
})

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

// Auth Login Ajax
$('#auth_loginform').submit(function (event) {
    event.preventDefault();
    console.log('Ajax Login');
    $.ajax({
        url: "/accounts/login/",
        data: $(this).serialize(),
        dataType: 'json',
        method: 'POST',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            var resp = data.responseJSON
            var errors = $('#form_errors');
            var loader = $('#form_loader');
            errors.html('');
            loader.removeClass('is-hidden');
            // Short timeout to signify that request went through
            setTimeout(function () {
                loader.addClass('is-hidden');
                errors.html(resp.form.errors);
            }, 250)
        },
    })
});

// Auth Signup Ajax
var signup = $('#auth_signupform')
var submit_button = $('#submit-id-submit')
var loader = $('#signupform_loader')
signup.submit(function (event) {
    event.preventDefault();
    submit_button.addClass('is-hidden');
    loader.removeClass('is-hidden');
    $.ajax({
        url: "/accounts/signup/",
        data: $(this).serialize(),
        dataType: 'json',
        method: 'POST',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            // Short timeout to signify that request went through
            setTimeout(function () {
                $.each(data.responseJSON.form.fields, function (key, element) {
                    loader.addClass('is-hidden');
                    submit_button.removeClass('is-hidden');
                    var field = $('#' + key + "_errors");
                    field.html(element.errors);
                });
            }, 250)
        }
    })
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

var errorNotify = function (msg) {
    n = new Noty({
        text: "<p class='subtitle is-5 has-text-light'>We have a problem...</p><p>" + msg + "</p>",
        theme: 'metroui',
        type: 'error',
        layout: 'topRight',
        closeWith: ['click', 'button'],
        timeout: 6000,
        killer: true,
    })
    return n
}

var infoNotify = function (title, msg) {
    n = new Noty({
        text: "<p class='subtitle is-5 has-text-light'>" + title + "</p><p>" + msg + "</p>",
        theme: 'metroui',
        type: 'info',
        layout: 'topRight',
        closeWith: ['click', 'button'],
        timeout: 6000,
        killer: true,
    })
    return n
}

// WIP function to handle the multiple ajax requests
var handleAjax = (function () {

    // Serialize form data and append CSRF token
    var prepareData = function (el) {
        var data = el.serializeArray();
        data.push({
            name: 'csrfmiddlewaretoken',
            value: getCookie('csrftoken')
        })
        return data
    };

    // Add Custom Data
    var appendData = function (data, additions) {
        data.push(additions)
        return data
    }

    // Submit Form Request
    var submitForm = function (el, data, success, error) {
        $.ajax({
            url: el.attr('action'),
            type: el.attr('method'),
            data: data,
            dataType: 'json',
            success: success,
            error: error,
        })
    }

    // Submit Request
    var submitRequest = function (el, data, success, error) {
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
        prepareData: prepareData,
        appendData: appendData,
        submitForm: submitForm,
        submitRequest: submitRequest
    };

})

// Load Cleave
var loadCleave = function () {
    // Detect
    var load = function () {
        var phone_sel = $('.js-phone-input');
        var date_sel = $('.js-date-input');
        $.each(phone_sel, function () {
            phone();
        })
        $.each(date_sel, function () {
            date();
        })
    }

    // Phone Input
    var phone = function () {
        var cleave = new Cleave('.js-phone-input', {
            phone: true,
            phoneRegionCode: 'US'
        });
    }

    // Date Input (month/year)
    var date = function () {
        var cleave_date = new Cleave('.js-date-input', {
            date: true,
            datePattern: ['m', 'y']
        });
    }

    return {
        load: load,
        date: date,
        phone: phone
    }
}

// Search Bar Creation
var timeout;
var SearchBar = function (el, page_func, success, error) {
    this.element = el || new jQuery();
    this.reload = page_func
    this.success = success || false
    this.error = error || false
}
SearchBar.prototype.bindEvents = function () {
    var input = $(this.element)
    var reload = this.reload
    var target_id = '#' + input.attr('search-target')
    var target = $(target_id)
    var baseHTML = target.html();
    if (!this.success) {
        var success = function (data) {
            console.log(data)
            target.html(data);
            reload();
        }
    } else {
        var success = this.success
    }
    if (!this.error) {
        var error = function (data) {
            target.load(document.URL + ' ' + target_id + ">*", function () {
                reload();
            })
        }
    } else {
        var error = this.error
    }
    input.on('keyup', function () {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
                handleAjax().submitRequest(input, input.serialize(), success, error)
            },
            400
        );
    })
}

// Device Tiles
var DeviceTiles = (function () {
    var search_input = $('.js-search-bar')
    var search = new SearchBar(search_input, function () {
        DeviceTiles().Repair();
    }, function (data) {
        var devices = data['device']
        var family = data['family']
        var $cards = $('div[data-device]')
        var $divids = $('div.is-divider[brand-id]')
        var brands = []
        var filter = function (callback) {
            var $tiles = $($cards.closest('.tile.is-parent'))
            $tiles.hide('fade', 500);
            $divids.hide('fade', 500);
            $cards.each(function (pos, card) {
                var pk = parseInt($(card).attr('data-device'))
                var $tile = $($(card).closest('.tile.is-parent'))
                var tile_brand = $tile.attr('brand-id')
                var $divider = $('div.is-divider[brand-id=' + tile_brand + ']')
                if (jQuery.inArray(tile_brand, brands) == -1) {
                    brands.push(tile_brand)
                }
                if ($(card).attr('data-family') == 'True') {
                    var array = family
                } else {
                    var array = devices
                }
                if (jQuery.inArray(pk, array) == -1) {
                    $tile.show('fade', 500);
                    $divider.show('fade', 500)
                }
            })
        }
        filter()
    }, function (data) {
        var $cards = $('div[data-device]')
        var $tiles = $($cards.closest('.tile.is-parent'))
        $tiles.hide('fade', 500);
        setTimeout(function () {
            $tiles.show('fade', 500);
        }, 500)
    })
    search.bindEvents();

    // Repair Tiles
    var Repair = function () {
        // Init
        var prev_top = 0;
        var hover_card = $('.is-hover-card')
        // Bind Hover cards to open
        hover_card.on('click', function (e) {
            close_all(hover_card)
            if ($(this).parent().children('div.has-info-triangle').length == 0) {
                open($(this))
            } else {
                var info_block = $(this).parent().find('.info-block')
                toggle_block(info_block, '0')
            }
        })

        // Get Info
        var get_info = function (tile, success_callback) {
            var request = handleAjax();
            var data = request.prepareData(tile);
            var device_data = {
                name: 'device',
                value: tile.attr('data-device')
            }
            data = request.appendData(data, device_data)
            if (tile.attr('data-family')) {
                data = request.appendData(data, {
                    name: 'family',
                    value: 1
                })
            }
            var error = function (data) {
                console.log('fail');
            }
            request.submitRequest(tile, data, success_callback, error)
        }

        // Close Others
        var close_all = function (tile) {
            // Vars
            var def_height = tile.height();
            // 
            $('.has-info-triangle').slideToggle('slow', function () {
                $(this).remove();
            });
            tile.css('height', def_height)
        }

        var toggle_block = function (block, margin) {
            block.animate({
                marginBottom: margin
            }, function () {
                //block.removeClass('is-active')
                if (margin == "0") {
                    block.attr('style', '')
                }
            })
        }

        // Open Tile
        var open = function (tile) {
            // Vars
            var info_block = tile.parent().find($('.info-block'))
            get_info(tile, function (info_element) {
                var $info_element = $(info_element)
                var width = $('#device-tiles-parent').width();
                // Get Objects
                var parent = tile.parent();
                var tri_pos = tile.position().left;
                // Append Info Element
                info_block.before($info_element);
                // Determine Whether or not we are on a new row
                var top = $info_element.position().top
                if (prev_top != top && prev_top != 0) {
                    toggle_block($('.info-block.is-active'), '0')
                    $('.info-block.is-active').removeClass('is-active')
                }
                prev_top = top
                info_block.addClass('is-active')
                // Position Indicator
                $('<style>.has-info-triangle:before{left:' + tri_pos + ';}</style>').appendTo('head');
                $info_element.css('left', '0');
                $info_element.css('width', width);
                // Animate Info Element Open
                $info_element.toggle();
                toggle_block(info_block, '300')
                $info_element.slideToggle();
            })
        }
    }
    return {
        Repair: Repair
    }
})