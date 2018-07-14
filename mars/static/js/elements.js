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


// Filter Menu
var FilterMenu = function (el) {
    this.element = el || new jQuery();
}

FilterMenu.prototype.bindEvents = function () {
    var el = this.element
    var filters = el.find('a[data-filter]')
    var type_filters = el.find('a[data-filter=type]')
    var brand_tiles = $('div[brand-id]')

    var sections = (function ($filter) {
        var active = get_target($filter)

        var get = function () {
            all = []
            $(type_filters).each(function (pos, el) {
                var target = get_target($(el))
                if (target != false) {
                    all.push(get_target($(el)))
                }
            })
            return all
        }

        var hide = function () {
            change(function ($sec) {
                $sec.hide('fade', 250)
            })
        }

        var showAll = function () {
            change(function ($sec) {
                $sec.show('fade', 250)
            })
        }

        var change = function (action) {
            type_filters.removeClass('is-active');
            $(get()).not(active).each(function (pos, el) {
                var sec = $(el)
                if (sec.length > 0) {
                    action(sec);
                }
            })
            $filter.addClass('is-active')
            active.show('fade', 250)
        }

        if (!active) {
            showAll();
        }

        return {
            hide: hide
        }
    })


    var get_target = function ($filter) {
        var $tar = $('#' + $filter.attr('data-value'))
        if ($tar.length > 0) {
            return $tar
        }
        return false
    }

    filters.on('click', function (e) {
        e.preventDefault();
        if ($(this).attr('data-filter') == 'type') {
            sections($(this)).hide();
        } else {
            $(this).toggleClass('is-active')
            //tiles($(this)).tog();
        }
    })
}

$(document).ready(function () {
    // Find Hidden menu elements
    var menu_elements = $('.js-hidden-menu')
    var menus = new HiddenMenu(menu_elements)
    menus.bindEvents();
    // Find Filter Menu elements
    var filter_elements = $('.js-filter-menu')
    var filters = new FilterMenu(filter_elements)
    filters.bindEvents();
})