// Payment Selection Widget
$.widget('payment.source_select', {
    _create: function () {
        var obj = this
        this.source_data = $('input[data-source=' + this.element.attr('id') + ']')
        this.target = $("div[data-source-target]")
        this.data = {
            method: "Card",
            brand: this.source_data.attr('data-source-brand'),
            name: this.source_data.attr('data-source-name'),
            last4: this.source_data.attr('data-source-last4')
        }
        this.element.on('click', function () {
            obj.update();
        })
    },
    update: function () {
        var children = this.target.children($('p[data-source-target]'))
        $.map(this.data, function (value, type) {
            var target = children.filter("[data-source-target=" + type + "]")
            target.html(value)
            return true
        })
    }
})


// Checkout Page Core Module
var CheckoutPage = (function () {

    var init = (function () {
        // Create Source Select Widgets
        $('input[name=payment_method_card]').source_select();
        // Load Form Reveal
        var $rev = $('.js-form-reveal')
        var $form = $rev.find('div#form')
        var $trig = $rev.children('a')
        var $close = $form.find('a[form-close]')
        $trig.add($close).on('click', function (e) {
            e.preventDefault();
            $trig.toggle('fade', 600, function () {
                $form.toggle('blind', 600, function () {
                    $rev.toggleClass('is-active')
                })
            })
        })
    })()

    console.log('Checkout page loaded')
})();