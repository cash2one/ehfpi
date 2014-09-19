/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {

    // get current sort option
    $('th[name]').css('background-image', 'url(/static/images/up_down.gif)');
    var url = location.search;
    var paraString = url.substring(1, url.length).split('&');
    for (var i = 0; i < paraString.length; i++) {
        var parms = paraString[i].split('=');
        if (parms[0] == 'order_by')  //get the order_by parm
        {
            var parm = parms[1];
            if (parms[1].substring(0, 1) == '-') {
                parm = parms[1].substring(1, parms[1].length);
                $('th[name=' + parm + ']').css('background-image', 'url(/static/images/down.gif)');
            } else {
                $('th[name=' + parm + ']').css('background-image', 'url(/static/images/up.gif)');
            }

            //change the opacity
            $('img[name=' + parms[1] + ']').css('opacity', '0.1');
        }
    }

    $("input[id='drugSubmitted']").prop("checked", true);
    $("input[id='selectAllColumnsSubmitted']").prop("checked", true);

});

//select all rows of current page
function selectCurrentPage(item) {
    $("input[name='tableRowCheckBox']").prop("checked", $(item).prop("checked"));
    if ($(item).prop("checked") == false) {
        $('#selectAllPage').prop("checked", false);
    }
    updateSelectNumber();
}

//select rows of all pages, including those not displayed
//it seems that it is the same with selectCurrentPage, we will check the state of this checkbox
function selectAllPage(item) {
    $('#selectCurrentPage').prop("checked", $(item).prop("checked"));
    $("input[name='tableRowCheckBox']").prop("checked", $(item).prop("checked"));
    updateSelectNumber();
}

//check if not all selected, just uncheck the selectCurrentPage and selectAllPageCheckbox
function stillSelectAll(item) {
    if ($(item).prop("checked") == false) {
        $('#selectCurrentPage').prop("checked", false);
        $('#selectAllPage').prop("checked", false);
    }
    updateSelectNumber();
}

//update select number
function updateSelectNumber() {
    var number = 0
    if ($('#selectAllPage').prop("checked") == true) {  //all pages
        number = $('#resultNumber').text();
    } else {
        $("input[name='tableRowCheckBox']").each(function (row) {
            if ($(this).prop("checked") == true) {
                number += 1;
            }
        });
    }
    $('#selectNumber').text(number);
    selectedNumber = number;
}

//replace all function
String.prototype.replaceAll = function (s1, s2) {
    return this.replace(new RegExp(s1, "gm"), s2);
}

//number of selected row
selectedNumber = 0;

//drug analysis
function performFunction(item) {

    //first check is there any data selected
    //var selectedNumber = $('#selectNumber')
    if (selectedNumber > 0) {
        //check the state of select
        var selected;
        var type;
        var columns = "";
        //get the selected items
        if ($('#selectAllPage').prop("checked")) {  //select all rows
            type = "all";
            //selected = new Array();
            //selected = $('#ids').text().split(',');
            //parse url address, same in search change columns
            var url = window.location.search.substr(1);
            var urlList = url.split("&");
            for (var i = 0; i < urlList.length; i++) {
                var index = urlList[i].indexOf('=');
                var myKey = urlList[i].substr(0, index);
                var myValue = urlList[i].substr(index+1);
                if (myKey == 'columns') {  //in the url
                    columns = myValue;
                }
                if (myKey == "jsTreeList") {
                    selected = myValue;
                }
            }
            columns = columns.replaceAll("%2C", ",");
            selected = selected.replaceAll("%2C", ",");

        } else {  //only current page
            type = "current";
            selected = new Array();
            columns = "";
            $("input[name='tableRowCheckBox']").each(function () {
                if ($(this).prop("checked")) {
                    selected.push($(this).val());
                }
            });
        }
        var functionType = item;
        if (functionType == "download") {  //download data
            $.fileDownload(URL_PREFIX + '/analysis/gwas/download?selected=' + selected + '&type=' + type+ '&columns='+columns)
                .done(function () {
                })
                .fail(function () {
                    alert('File download failed!');
                });

        }

    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
    }
}

//change state of checkbox
function changeState(item, type) {
    if (type == 'submitted') {
        $("input[id='drugSubmitted']").prop("checked", $(item).prop("checked"));
    } else {
        $("input[id='drugOthers']").prop("checked", $(item).prop("checked"));
    }
}

//check if not all selected, just uncheck select all
function stillSelectAllFilter(item, type) {
    if ($(item).prop("checked") == false) {
        if (type == "submitted") {
            $('#selectAllColumnsSubmitted').prop("checked", false);
        } else {
            $('#selectAllColumnsOthers').prop("checked", false);
        }
    }
}

columns = new Array();
//custom filter columns
function filterTable(item) {
    columns.length = 0; //empty the array
    $("input[name ='drugColumn']").each(function () {
        if ($(this).prop("checked")) {
            columns.push($(this).val());
        }
    });

    //parse url address, same in search change columns
    var url = window.location.search.substr(1);
    var urlList = url.split("&");
    //console.log(urlList);
    var columnIn = 0;
    for (var i = 0; i < urlList.length; i++) {
        var index = urlList[i].indexOf('=');
        var myKey = urlList[i].substr(0, index);
        if (myKey == 'columns') {  //in the url
            columnIn = 1;
            urlList[i] = 'columns=' + columns;
            break;
        }
    }
    if (columnIn == 0) {
        url = window.location.href + '&columns=' + columns;
    } else {
        url = window.location.pathname + '?' + urlList.join("&");
    }
    //console.log(url);
    window.location.href = url;
}
