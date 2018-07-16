requirejs.config({
    baseUrl: '/static/js/lib',
    paths: {
        jquery: 'jquery',
        jqueryui: 'jquery-ui',
        Noty: 'noty.min',
        app: '/static/js/app'
    }
});

// Require Scripts Used Cross Site
requirejs(['jquery'], function ($) {
    requirejs(['jqueryui', 'bulma'])
    // Setup Cleave
    requirejs(['cleave'], function (cleave) {
        requirejs(['cleave-phone.us'], function () {
            requirejs(['app/libs/cleave-setup'])
        })
    })
    // Noty
    requirejs(['Noty'], function (Noty) {
        requirejs(['app/libs/noty-setup'], function (Notify) {})
    })
    // Navbar
    requirejs(['app/nav'])
});