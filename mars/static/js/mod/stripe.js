// Stripe Elements Handler

$.widget('handlestripe.stripe_card', {
    options: {
        stripe_key: 'pk_test_LEe8SgXbnZz4zkFlVCTlmZlF',
        style: {
            base: {
                fontSize: '18px',
                color: "#32325d"
            }
        },
        selectors: {
            mount: '.js-stripe-card',
            errors: '#stripe-errors',
        }
    },
    _create: function () {
        var obj = this
        this.stripe = Stripe(this.options.stripe_key)
        this.container = this.element.parents('.card-content')
        console.log(this.container)
        this.card = this.stripe.elements().create('card', {
            style: obj.options.style
        })
        this.card.mount(this.options.selectors.mount)
        this.errors = $(this.options.selectors.errors)
        this.card.on('change', function (e) {
            if (e.error) {
                obj.errors.html(e.error.message)
            } else {
                obj.errors.html('')
            }
        })
        this.element.on('submit', function (e) {
            e.preventDefault();
            obj._handle();
        })
    },
    _handle: function () {
        var obj = this
        this.stripe.createToken(this.card).then(function (result) {
            if (result.error) {
                console.log('error')
                obj.errors.html(result.error.message)
            } else {
                obj._handle_token(result.token)
                console.log('passed')
            }
        })
    },
    _handle_token: function (token) {
        var obj = this
        var request = HandleAjax(this.element, function (data) {
            if (saved) {
                location.reload();
            } else {
                obj.data = data
                obj._handle_tempcard();
            }
        })
        var saved = request.data.find(x => x.name === "save_card")
        request.data.push({
            name: 'stripeToken',
            value: token.id
        })
        if (saved) {
            request.data.push({
                name: 'save_card',
                value: true
            })
        }
        request.submit();
    },
    _handle_tempcard: function () {
        var obj = this
        this.container_base = this.container.html()
        this.container.find('.is-header').attr('data-content', 'Unsaved Card')
        this.container_card = this.container.find('.columns.is-multiline')
        this.container.find($('.columns')).hide('fade', 600, function () {
            obj.container_card.html(obj.data)
        })
        obj.$cancel_temp = $('<a>Cancel</a>')
        obj.container_card.after(obj.$cancel_temp)
        this.container_card.show('fade', 600, function () {
            var source = $(this).find('input[name=payment_method_card]').source_select();
            source.source_select('update');
            obj.$cancel_temp.on('click', function (e) {
                obj.container.effect('fade', 600, function () {
                    obj.container.html(obj.container_base)
                })
            })
        })

    }
})

// Stripe Handler Module
var HandleStripe = (function () {
    $(document).ready(function () {
        $('.js-stripe-form').stripe_card();
        console.log('stripe loaded')
    })
})()