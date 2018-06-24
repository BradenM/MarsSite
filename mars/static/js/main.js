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


var accountPage = (function () {

    // Vars
    var content = $('#account-view')
    var account_sel = $('a[load-account]')
    var contentWindow = $('.Site-content').height();
    var track_links = $('a[load-tracker]');


    // Init
    account_sel.click(function (e) {
        loadPage($(this));
    })

    // Page Selection
    var loadPage = function (sel) {
        // Select Link
        var link = $(sel);
        account_sel.each(function () {
            $(this).removeClass('is-active');
        })
        link.addClass('is-active')
        // Load Page
        var page_url = link.attr('load-account') + "/";
        content.load(page_url, function () {
            adjustScroll();
            Search($('input[search-data]'));
            loadTracker(track_links);
            AccountSettings();
        })
    }

    // Adjust Scroll for lists
    var adjustScroll = function () {
        var el = $('section[data-scroll-adjust]')
        var footer = $("footer").height();
        var adjust = contentWindow - footer * 2;
        console.log(contentWindow, footer, adjust);
        el.css('overflow-y', 'auto');
        el.css('max-height', adjust);
    }

    // Get Tracker info for orders
    var loadTracker = function (links) {
        links.on('click', function (e) {
            var track = $(e.target).attr('load-tracker');
            var url = "tracker/" + track;
            content.load(url, function () {
                accountPage();
            });
        })
    }
})

var Search = function (sel) {
    var input = $(sel)
    var target = $('#' + input.attr('search-target'))
    var baseHTML = target.html();
    input.on('change, paste, keyup', function () {
        $.ajax({
            url: input.attr('search-data'),
            data: $(this).serialize(),
            method: 'GET',
            success: function (data) {
                target.html(data);
            },
            error: function (data) {
                target.html(baseHTML);
            }
        })
    })
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

var AccountSettings = (function () {
    // Init

    // Unlock Input
    $('a[data-unlock]').click(function (e) {
        unlockInput($(this));
    });

    // Allow Input Modify
    var unlockInput = function (trig) {
        var target_sel = trig.attr("data-unlock");
        var target_inp = $('#' + target_sel);
        // Allow Edit
        target_inp.removeAttr('readonly');
        // Change Trigger to 'save' and rebind
        trig.html('Save');
        // Unbind
        trig.off();
        // Bind to save
        trig.click(function (e) {
            saveInput(trig);
        })
    }

    // Save Input via Ajax
    var saveInput = function (trig) {
        var target_sel = trig.attr('data-unlock');
        var target_inp = $('#' + target_sel);
        // Get Form info
        var form = $('#' + target_inp.attr('form'))
        var form_data = form.find('input');
        var form_success = form.find('input[id=submit-id-submit]').attr('value');
        console.log(form_success)

        // Catch form post
        form.on('submit', function (e) {
            e.preventDefault();
            form_data.val(target_inp.val()); // Set new input to form val
            var ajax_data = form.serializeArray();
            // Append add action data for adding email
            ajax_data.push({
                name: 'action_add',
                value: ''
            })
            // Append CSRF token cookie
            ajax_data.push({
                name: 'csrfmiddlewaretoken',
                value: getCookie('csrftoken')
            })
            $.ajax({
                url: form.attr('action'),
                type: form.attr('method'),
                data: ajax_data,
                dataType: 'json',
                success: function (data) {
                    target_inp.attr('readonly', '');
                    trig.html('Change');
                    // rebind
                    trig.off();
                    trig.click(function (e) {
                        unlockInput(trig);
                    })
                    n = infoNotify('Success!', form_success)
                    n.show();
                },
                error: function (data) {
                    console.log(data);
                    var json_fields = data.responseJSON.form.fields
                    //n = errorNotify(json_fields.email.errors);
                    var error_msg = []
                    $.each(json_fields, function (key, field) {
                        error_msg.push(field.errors);
                    })
                    n = errorNotify(error_msg);
                    n.show();
                }
            })
        })

        // Submit
        form.submit();

    }

    // Change Password Ajax
    var loadChangePassword = function () {
        var change_passform = $('#auth_changepass');
        var loader = $('#pc_loader');
        var submit_button = $('#pcsubmit');
        change_passform.on('submit', function (e) {
            e.preventDefault();
            submit_button.addClass('is-hidden');
            loader.removeClass('is-hidden');
            $.ajax({
                url: change_passform.attr('action'),
                type: "POST",
                dataType: 'json',
                data: change_passform.serialize(),
                success: function (data) {
                    location.reload();
                },
                error: function (data) {
                    console.log(data.responseJSON.form.fields);
                    // Short timeout to signify that request went through
                    setTimeout(function () {
                        $.each(data.responseJSON.form.fields, function (key, element) {
                            loader.addClass('is-hidden');
                            submit_button.removeClass('is-hidden');
                            var field = $('#pc_' + key + "_errors");
                            console.log(field);
                            field.html(element.errors);
                            console.log(element.errors);
                        });
                    }, 250)
                }
            })
        })
    }

})

$(document).ready(function () {
    accountPage();
});