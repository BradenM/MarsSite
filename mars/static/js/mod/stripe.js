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
        this.container = this.element.parents('.card')
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
        this.pages = this.container.find('.card-content')
        this.temp_page = this.pages.not('.is-active').find('.js-page-inject')
        this.pages.filter('.is-active').effect('fade', 1000, function () {
            obj.temp_page.html(obj.data)
            obj.pages.toggleClass('is-active')
        });
    }
})

// Stripe Handler Module
var HandleStripe = (function () {
    $(document).ready(function () {
        $('.js-stripe-form').stripe_card();
        console.log('stripe loaded')
    })
})()