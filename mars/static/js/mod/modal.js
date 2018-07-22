// User Login/Signin Modal
var UserModal = (function () {
    // Variables
    var $sel = $('.js-user-modal');
    var triggers = $sel.filter('[data-modal=trigger]')
    var $modal = $sel.filter('[data-modal=modal]')
    var $tabs = $($modal.find($('.tabs li')))
    var $windows = $($modal.find($('.tab-child')))
    var $submit = $($modal.find($('input[data-modal]')))
    var $loader = $('.form_loader');

    // Submit either form
    var submit = function ($form) {
        var is_signup = (function () {
            var attr = $form.attr('id');
            if (attr == 'auth_signupform') {
                return true
            }
        })();
        $form.on('submit', function (event) {
            event.preventDefault();
            var request = HandleAjax($form, function (data) {
                location.reload()
            }, function (data) {
                var resp = data.responseJSON
                var errors = $('#form_errors')
                errors.html('');
                $submit.hide('fade', 50)
                $loader.show('fade', 50)
                setTimeout(function () {
                    $submit.show('fade', 50)
                    $loader.hide('fade', 50)
                    if (is_signup) {
                        $.each(data.responseJSON.form.fields, function (key, element) {
                            var field = $('#' + key + "_errors");
                            field.html(element.errors);
                        });
                    } else {
                        errors.html(resp.form.errors);
                    }
                }, 250)
            })
            request.submit();
        })
        $form.submit();

    }

    // Init
    var init = function () {
        // Open/Close Modal
        $(triggers).on('click', function () {
            $modal.toggleClass('is-active');
        })
        // Change Tab
        $tabs.on('click', function () {
            $tabs.toggleClass('is-active')
            $windows.toggleClass('is-active');
        })
        // Submit
        $submit.on('click', function (e) {
            e.preventDefault();
            var target = $('#' + $(this).attr('data-modal'))
            console.log(target)
            submit(target)
        })
    }

    return {
        init: init,
    }

})

// Load needed functions on page  load
$(document).ready(function () {
    UserModal().init()
})