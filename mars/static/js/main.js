$(document).ready(function(){
    console.log('Main Script file loaded');

    jQuery.fn.extend({
        aniscroll: function(){
            $(this).animatescroll({scrollSpeed:1500,easing:'easeInOutSine'});
        }
    })

})
