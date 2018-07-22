// Hidden Menu Element
var HiddenMenu = function (el) {
    this.element = el || new jQuery();
}
HiddenMenu.prototype.bindEvents = function () {
    var el = this.element
    var trigger = el.find('a[data-menu=trigger]')
    var menu = el.find('div[data-menu=content]')

    var toggleOpen = function ($button) {
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
    var clear_filter = el.find('button[data-filter=clear]')

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
            hide: hide,
            showAll: showAll
        }
    })

    var tiles = (function () {
        var brand_tiles = $('div[brand-id]')

        var get = function () {
            visible = []
            filters.each(function (pos, filter) {
                var $fi = $(filter)
                if ($fi.attr('data-filter') == 'brand' && $fi.hasClass('is-active')) {
                    visible.push($fi)
                }
            })
            if (visible.length <= 0) {
                clear();
            }
            return visible
        }

        var clear = function () {
            $(brand_tiles).show('fade', 250);
            $(filters).not(type_filters).each(function () {
                if (!$(this).hasClass('is-active')) {
                    $(this).find('.panel-icon').toggle();
                    $(this).toggleClass('is-active')
                }
            })
        }

        var update = function () {
            var brand_tiles = $('div[brand-id]')
            $(brand_tiles).hide('fade', 250, function () {
                $(this).css('display', 'none')
            });
            $(get()).each(function (pos, filter) {
                var $fi = $(filter)
                var $fi_targ = $('div[brand-id=' + $fi.attr('data-value') + ']')
                $fi_targ.show('fade', 250);
            })

        }

        return {
            update: update,
            clear: clear
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
        if ($(this).attr('data-filter') == 'type') {
            sections($(this)).hide();
        } else {
            $(this).find('.panel-icon').toggle();
            $(this).toggleClass('is-active')
            tiles().update();
        }
    })

    clear_filter.on('click', function () {
        tiles().clear();
        sections($(type_filters).first()).showAll();
    })
}

// Search Bar Element
var timeout;
var SearchBar = function (el, page_func, success, error) {
    this.element = el || new jQuery();
    this.reload = page_func
    this.success = success || false
    this.error = error || false
}

SearchBar.prototype.bindEvents = function () {
    var input = $(this.element)
    var reload = this.reload || function () {
        console.log('search complete')
    }
    var target_id = '#' + input.attr('search-target')
    var target = $(target_id)
    var baseHTML = target.html();
    if (!this.success) {
        var success = function (data) {
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
                var request = HandleAjax(input, success, error)
                request.submit()
            },
            400
        );
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