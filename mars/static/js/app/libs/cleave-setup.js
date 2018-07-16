var phone = $('.js-phone-input')
var date = $('.js-date-input')

$(phone).each(function (pos, el) {
    var cleave = new Cleave($(el), {
        phone: true,
        phoneRegionCode: 'US'
    })
})

$(date).each(function (pos, el) {
    var date = new Cleave($(el), {
        date: true,
        datePattern: ['m', 'y']
    })
})