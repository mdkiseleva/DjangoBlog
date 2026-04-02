$(document).ready(function(){
    var yPosition;
    var scrolled = 0;
    var $parallaxElements = $('.icons-for-parallax img');
    $(window).scroll(function() {
        scrolled = $(window).scrollTop();
        for (var i = 0; i < $parallaxElements.length; i++){
            yPosition = (scrolled * 0.15*(i + 1));
            $parallaxElements.eq(i).css({ top: yPosition });
        }
    });
});

$(document).ready(function(){
    var $logo = $('.logo');

    $(window).scroll(function() {
        var scrolled = $(window).scrollTop();

        $logo.css({
            top: scrolled * 0.5
        });
    });
});