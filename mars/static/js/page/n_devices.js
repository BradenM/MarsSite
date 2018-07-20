// Tile Widget
$.widget('devices.device_tile', {
    _create: function () {
        this.parent_tile = this.element.parent().parent()
        this.parent_tile.row = $(this.parent_tile).add(this.parent_tile.siblings())
        var obj = this
        var request = HandleAjax(this.element, function (data) {
            obj.data = data
            obj._attach();
        }, null)
        request.data = request.data.push({
            name: 'device',
            value: this.element.attr('data-device')
        })
        request.submit();
    },

    _is_family: function () {
        if (this.element.attr('data-family')) {
            return true
        } else {
            return false
        }
    },

    _attach: function () {
        var obj = this
        this.section = $(this.data)
        this.element.after(this.section)
        this.section.hide();
        this.section.shown = false;
        this.element.on('click', function () {
            obj.toggle();
        })
    },

    _get_row: function () {
        obj = this
        this.parent_tile.row = this.parent_tile.row.map(function (pos, el) {
            var $el = $(el)
            if ($el.position().top == obj.parent_tile.position().top) {
                return $el
            }
        })
    },

    _position_indicator: function (callback) {
        this.indicator = this
        this.indicator.position = this.element.position().left
        this.indicator.style = $('<style>.has-info-triangle.active:before{left:' + this.indicator.position + ';}</style>')
        this.indicator.style.appendTo('head')
        callback();
    },

    _insert_margin: function () {
        obj = this
        var $last = this.parent_tile.row[this.parent_tile.row.length - 1]
        this.margin = $('<div></div>')
        $last.after(this.margin)
        this.margin.addClass('is-block-divider')
        this.margin.addClass('active', 400)
    },

    hide_other: function (callback) {
        var obj = this
        var others = $(':devices-device_tile').not(this.element)
        $(others).each(function (pos, el) {
            var inst = $(el).device_tile('instance')
            if (inst.section && inst.section.shown) {
                inst.hide();
            }

        })
        callback();
    },

    hide: function () {
        this.section.hide('blind', 400)
        this.section.shown = false
        this.indicator.style.remove();
        var obj = this
        if (this.margin) {
            this.margin.removeClass('active', 400, function () {
                obj.margin.remove();
            })
        }
    },

    toggle: function () {
        this._get_row();
        var obj = this
        this.hide_other(function () {
            if (!obj.section.shown) {
                obj._insert_margin()
                obj._position_indicator(function () {
                    obj.section.show('blind', 400, function () {
                        obj.section.shown = true
                        obj.section.addClass('active', 1000)
                    })
                });
            } else {
                obj.hide();
            }
        })
    }
});

// View Devices (View Devices Page)
var ViewDevices = (function () {
    var $tiles = $('.is-hover-card').not('[data-family=True]').device_tile();

    var tiles = function () {
        console.log('tiles loaded')
    }
    return {
        tiles: tiles()
    }
})();