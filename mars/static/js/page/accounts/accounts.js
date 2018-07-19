// Core Module for User Accounts
var UserAccounts = (function () {
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
    var updateMenu = function () {
        var path = location.pathname
        var selectors = $('.menu li a')
        $.each(selectors, function () {
            if (path == $(this).attr('href')) {
                $(this).addClass('is-active');
                return false;
            }
        })
    }

    return {
        adjustScroll: adjustScroll,
        updateMenu: updateMenu,
    }
});

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
                Notify('Phone number changed successfully', "Success").info();
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
var Settings = (function (UserAccounts) {
    var _$sel = $('a[data-unlock]')

    // Retunr Module
    UserAccounts.settings = function () {
        _$sel.each(function (pos, el) {
            var $el = $(el)
            var toggle = new UserAccounts.elements.ToggleInput($el)
            toggle.bindEvents();
        })
    }
    return UserAccounts

})(UserAccounts || {});