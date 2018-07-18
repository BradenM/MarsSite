// Device Tiles ( View Devices Page)
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
            var request = HandleAjax();
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