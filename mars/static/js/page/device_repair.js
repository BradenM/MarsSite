// Repair Tile Widget
$.widget('devices.repair_tile', {
    _create: function () {
        var obj = this
        this.repair_pk = this.element.attr('data-repair')
        this.target = $('#repair_details')
        this.ajax_parent = this.element.parents('.card-content')
        console.log(this.ajax_parent)
        this.element.on('click', function () {
            obj.load();
        })
    },
    _get: function (callback) {
        var obj = this
        var request = HandleAjax(this.ajax_parent, function (data) {
            obj.data = data
            callback()
        }, function (data) {
            console.log('error')
        })
        request.data = request.data.push({
            name: 'repair_pk',
            value: obj.repair_pk
        })
        request.submit()
    },

    _select: function () {
        var $siblings = $(':devices-repair_tile')
        $siblings.removeClass('is-active', 1000);
        this.element.addClass('is-active', 1000);
    },

    load: function () {
        var obj = this
        this._select();
        this._get(function () {
            console.log('got')
            obj.target.html(obj.data)
            ScrollTo(obj.target)
        })
    }
})

// DevicePage
var DevicePage = (function () {
    // Init
    var repair_tiles = $('.js-repair-tile').repair_tile()
    console.log('Device page Loaded')
})();