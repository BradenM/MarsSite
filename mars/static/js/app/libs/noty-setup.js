define(function () {
    var Notify = (function (msg, title) {
        var error = function () {
            var n = new Noty({
                text: "<p class='subtitle is-5 has-text-light'>We have a problem...</p><p>" + msg + "</p>",
                theme: 'metroui',
                type: 'error',
                layout: 'topRight',
                closeWith: ['click', 'button'],
                timeout: 6000,
                killer: true,
            })
            return n
        }

        var info = function () {
            var n = new Noty({
                text: "<p class='subtitle is-5 has-text-light'>" + title + "</p><p>" + msg + "</p>",
                theme: 'metroui',
                type: 'info',
                layout: 'topRight',
                closeWith: ['click', 'button'],
                timeout: 6000,
                killer: true,
            })
            return n
        }

        return {
            error: error,
            info: info
        }
    })
})