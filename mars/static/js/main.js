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
            loadChangePassword();
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

$(document).ready(function () {
    accountPage();
});