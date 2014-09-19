/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {
    var winWidth = 0;
    //set tp top position
    if (window.innerWidth)
        winWidth = window.innerWidth;
    else if ((document.body) && (document.body.clientWidth))
        winWidth = document.body.clientWidth;

    var conWidth = $('.container').css('width');
    conWidth = conWidth.substr(0,conWidth.length-2);
    $('.gotop').css({'right':(winWidth-conWidth)/2});


});


