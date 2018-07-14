// Hidden Menu Element
var HiddenMenu = function (el) {
    this.element = el || new jQuery();
}
HiddenMenu.prototype.bindEvents = function () {
    var el = this.element
    var trigger = el.find('a[data-menu=trigger]')
    var menu = el.find('div[data-menu=content]')

    var toggleOpen = function ($button, callback) {
        if (el.hasClass('is-active')) {
            menu.toggle('blind', 250)
        }
        el.toggleClass('is-active')
        $button.toggle('blind', 250, function () {
            $(this).toggleClass('is-active');
            var $status = $($(this).find('span').last())
            var $icons = $($button.find('span').not($status))
            if ($(this).hasClass('is-active')) {
                $status.html('Close')
                $icons.toggle();
            } else {
                $status.html('Search')
                $icons.toggle();
            }
            setTimeout(function () {
                $button.toggle('blind', 250, function () {
                    if (el.hasClass('is-active')) {
                        menu.toggle('blind', 250)
                    }
                });
            }, 300)
        })

    }

    trigger.on('click', function () {
        toggleOpen($(this))
    })
}

$(document).ready(function () {
    // Find and add Elements by class
    var menu_elements = $('.js-hidden-menu')
    var menus = new HiddenMenu(menu_elements)
    menus.bindEvents();
})