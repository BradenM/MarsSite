// Show and load user modal
define(function () {
    // Open Modal
    var trigger = $('.js-show-usermodal');
    var modal = $('#user_modal');
    trigger.on('click', function (e) {
        e.preventDefault();
        modal.addClass('is-active');
    })
    // Bind Tabs
    var $tabs = $(modal.find($('li#tab')));
    var $windows = $(modal.find($('div#tab_child')));
    $tabs.on('click', function () {
        $tabs.toggleClass('is-active');
        $tabs.each(function (pos, tab) {
            var $target = $('#' + $(tab).attr('data-target') + "_tab")
            $target.toggle('fade', 500)
        })
    })
})