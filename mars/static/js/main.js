var navigationFn = {
    goToSection: function(id) {
        $('html, body').animate({
            scrollTop: $(id).offset().top
        }, 0);
    }
}