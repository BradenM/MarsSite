// Core Module for User Accounts
var UserAccounts = (function () {
    // Pages
    var pages = {}

    // Adjust scrollabel div
    var adjustScroll = function () {
        var scrollDiv = $('section[data-scroll-adjust]');
        var tile = scrollDiv.find($('.is-child')).height();
        var tileNum = Math.ceil(scrollDiv.height() / tile)
        var tileAdjust = scrollDiv.height() - (tile * (tileNum - 4))
        scrollDiv.css('height', tileAdjust);
        scrollDiv.css('overflow-y', 'auto');
    }

    // Update Menu Nav
    var updateMenu = (function () {
        var path = location.pathname
        var selectors = $('.menu li a')
        $.each(selectors, function () {
            if (path == $(this).attr('href')) {
                $(this).addClass('is-active');
                return false;
            }
        })
    })();

    var load = function () {
        var current_p = $('section[data-user-page]').attr('data-user-page')
        if (current_p in pages) {
            pages[current_p]()
        }
    }

    return {
        pages: pages,
        load: load,
        adjustScroll: adjustScroll,
        updateMenu: updateMenu,
    }
})();


(function () {
    UserAccounts.elements = {
        ToggleInput: function (el) {
            this.element = el || new jQuery();
            this.target = $('#' + el.attr('data-unlock'))
            this.lock = true;
        }
    };
    UserAccounts.elements.ToggleInput.prototype = {
        toggle: function () {
            var obj = this
            if (obj.lock) {
                obj.target.removeAttr('disabled');
                this.element.html('Save');
            } else {
                obj.save();
                obj.target.attr('disabled', '')
                this.element.html('Change')
            }
            obj.lock = !obj.lock
            return this
        },
        save: function () {
            var obj = this;
            var request = HandleAjax(this.target, function (data) {
                var msg = obj.target.attr('data-success')
                Notify(msg, "Success").info();
            }, function (data) {
                var fields = data.responseJSON.form.fields
                var errors = []
                $.each(fields, function (key, field) {
                    errors.push(field.errors)
                })
                Notify(errors).error();
            })
            request.type = 'json'
            var input_data = {
                name: this.element.attr('name'),
                value: this.target.val()
            }
            request.data = request.data.push(input_data)
            request.submit();
        },
        bindEvents: function () {
            var obj = this
            this.element.on('click', function (e) {
                e.preventDefault();
                obj.toggle();
            });
        },
    }
})();



// User Settings Page
var Settings = (function (parent) {
    var _$sel = $('a[data-unlock]')

    // Settings Module
    UserAccounts.settings = function () {
        // Create Toggle Inputs
        _$sel.each(function (pos, el) {
            var $el = $(el)
            var toggle = new UserAccounts.elements.ToggleInput($el)
            toggle.bindEvents();
        })
        // Change Password Form
        var $form = $('.js-change-passwd').find($('form'))
        var $errors = $form.find('p.help')
        var $load = $form.find('a.is-loading')
        $form.on('submit', function (e) {
            $errors.html('')
            e.preventDefault();
            $load.removeClass('is-hidden')
            request = HandleAjax($form, function (data) {
                location.reload();

            }, function (data) {
                $load.addClass('is-hidden')
                var json_errors = data.responseJSON.form.fields
                $.each(json_errors, function (key, field) {
                    var er_field = $errors.filter('#' + key + "_error")
                    er_field.html(field.errors)
                })
            })
            request.submit();
        })
        return this
    }
    parent.pages.settings = UserAccounts.settings
    parent.load();
    return UserAccounts

})(UserAccounts || {});

// Card Payment Widget
$.widget('user.payment_card', {
    options: {
        buttons: {
            edit: ['Edit Card', 'Save'],
            remove: ['Remove Card', 'Cancel']
        }
    },
    _create: function () {
        var obj = this
        this.parent = this.element.parent()
        this.trigger = this.element.find('a.js-payment-toggle')
        this.content = this.element.find('div.card-content')
        this.edit_form = this.element.find('form')
        this.buttons = this.parent.find($('span.button'))
        this.remove_attr = $(this.buttons[1]).attr('onclick')
        this.controls = this.edit_form.find('div.control')
        this.controls.error = this.controls.parent().find('p.help');
        this.content.hide()
        this.trigger.on('click', function (e) {
            obj._toggle();
            e.preventDefault();
        })
        this.buttons.first().on('click', function () {
            obj._toggle_edit()
        })

    },
    _toggle: function () {
        var obj = this
        this.element.toggleClass('is-active');
        this.content.toggle('blind', 300)
    },

    _set_html: function ($button, option) {
        var current = $button.html()
        $.each(option, function (pos, opt) {
            if (current != opt) {
                $button.html(opt)
            }
        })
    },

    _toggle_edit: function () {
        var obj = this
        var edit = $(this.buttons[0])
        var remove = $(this.buttons[1])
        var def = $(this.buttons[2])
        def.toggle('fade', 300)
        edit.toggleClass('is-primary', 300)
        this._set_html(edit, this.options.buttons.edit)
        this._set_html(remove, this.options.buttons.remove)
        this.controls.children().toggle()
        edit.off()
        edit.on('click', function () {
            obj._save_card(edit)
        })
        if (remove.attr('onclick') == this.remove_attr) {
            remove.attr('onclick', '')
            remove.on('click', function () {
                obj._toggle_edit()
            })
        } else {
            obj.controls.error.html('')
            remove.off()
            remove.attr('onclick', this.remove_attr)
            edit.off()
            edit.on('click', function () {
                obj._toggle_edit();
            })
        }
    },

    _save_card: function ($edit) {
        var obj = this
        $edit.addClass('is-loading');
        var request = HandleAjax(this.edit_form, function (data) {
            location.reload()
        }, function (data) {
            $edit.removeClass('is-loading')
            obj.controls.error.filter('#date_error').html(data.responseJSON['date_errors'])
        })
        request.submit()
    }
})

// User Payments Page
var Payments = (function (parent) {
    // Payments Module
    UserAccounts.payments = function () {
        $('.js-payment-card').payment_card();
        return this
    }
    parent.pages.payments = UserAccounts.payments
    parent.load();
    return UserAccounts

})(UserAccounts || {});

// User Orders Page
var Orders = (function (parent) {
    // Orders Module
    UserAccounts.orders = function () {
        UserAccounts.adjustScroll();
        var search_input = $('input[search-target]')
        var search = new SearchBar(search_input);
        search.bindEvents();
        return this
    }
    parent.pages.orders = UserAccounts.orders
    parent.load();
    return UserAccounts

})(UserAccounts || {});

// User Orders Page
var Invoices = (function (parent) {
    // Orders Module
    UserAccounts.invoices = function () {
        UserAccounts.adjustScroll();
        var search_input = $('input[search-target]')
        var search = new SearchBar(search_input);
        search.bindEvents();
        return this
    }
    parent.pages.invoices = UserAccounts.invoices
    parent.load();
    return UserAccounts

})(UserAccounts || {});