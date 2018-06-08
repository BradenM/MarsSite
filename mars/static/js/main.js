$(document).ready(function(){
    console.log('Main Script file loaded');
    $('#signup_tab').hide();

    jQuery.fn.extend({
        // Animated Scroll
        aniscroll: function(){
            $(this).animatescroll({scrollSpeed:1500,easing:'easeInOutSine'});
        },
        // Hardcoded cause im lazy user tab switching function, will fix later
        switchTab: function(){
            var target = this
            console.log('tab switched');
            if (this.is('#signup_tab')){
                $('#signup_tab').show();
                $('#login_tab').hide();
                $('#login_tab_button').removeClass('is-active');
                $('#signup_tab_button').addClass('is-active');
            }
            else{
                $('#signup_tab').hide();
                $('#login_tab').show();
                $('#login_tab_button').addClass('is-active');
                $('#signup_tab_button').removeClass('is-active');
            }
            return(false);
        }

    })
})