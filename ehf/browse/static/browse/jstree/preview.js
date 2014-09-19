/**
 * Created by jacky on 14-4-3.
 */
$(function () {
    // get current sort option for table sort
    $('th[name]').css('background-image','url(/static/images/up_down.gif)');
    var url = location.search;
    var paraString = url.substring(1,url.length).split('&');
    for(var i=0;i<paraString.length;i++){
        var parms = paraString[i].split('=');
        if(parms[0] == 'order_by')  //get the order_by parm
        {
            var parm = parms[1];
            if(parms[1].substring(0,1)=='-'){
                parm = parms[1].substring(1,parms[1].length);
                $('th[name='+parm+']').css('background-image','url(/static/images/down.gif)');
            }else{
                $('th[name='+parm+']').css('background-image','url(/static/images/up.gif)');
            }

            //change the opacity
            $('img[name='+parms[1]+']').css('opacity','0.1');
        }
    }


});