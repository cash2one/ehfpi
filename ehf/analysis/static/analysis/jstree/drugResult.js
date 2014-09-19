/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {

    $('#gwasAnalysisTip').qtip({
        content: {
            title: 'Drug Target Analysis',
            text: 'You can download results of interests or directly visualize in a network representation.'
        },
        position: {
            my: 'top left',
            at: 'bottom right'
        },
        style: {
            classes: 'qtip-bootstrap'
        },
        show: {
            effect: function (offset) {
                $(this).slideDown(100); // "this" refers to the tooltip
            }
        },
        hide: {
            effect: function (offset) {
                $(this).slideDown(100); // "this" refers to the tooltip
            }
        }

    });

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
        var geneList = ""

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
                if (myKey == 'geneList') {  //in the url
                    geneList = myValue;
                }

            }
            columns = columns.replaceAll("%2C", ",");
            selected = selected.replaceAll("%2C", ",");
            geneList = geneList.replaceAll("%2C", ",");

        } else {  //only current page
            type = "current";
            selected = new Array();
            columns = "";
            geneList = ""
            $("input[name='tableRowCheckBox']").each(function () {
                if ($(this).prop("checked")) {
                    selected.push($(this).val());
                }
            });
        }
        var functionType = item;
        if (functionType == "download") {  //download data
            $.fileDownload(URL_PREFIX + '/analysis/drug/download?selected=' + selected + '&type=' + type+ '&columns='+columns+'&geneList='+geneList)
                .done(function () {
                })
                .fail(function () {
                    alert('File download failed!');
                });

        } else {//network

            openPostWindow(URL_PREFIX + '/analysis/drug/network/', type, selected,columns,geneList, URL_PREFIX + '/analysis/drug/network/');
            //window.open(URL_PREFIX+'/analysis/pip/network?selected=' + selected);
        }


    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
    }
}

//post into a new window
function openPostWindow(url, type, selected,columns,geneList, name) {
    var tempForm = document.createElement("form");
    tempForm.id = "tempForm1";
    tempForm.method = "post";
    tempForm.action = url;
    tempForm.target = name;

    var hideInput = document.createElement("input");
    hideInput.type = "hidden";
    hideInput.name = "type"
    hideInput.value = type;
    tempForm.appendChild(hideInput);

    var hideInput = document.createElement("input");
    hideInput.type = "hidden";
    hideInput.name = "selected"
    hideInput.value = selected;
    tempForm.appendChild(hideInput);

    var hideInput = document.createElement("input");
    hideInput.type = "hidden";
    hideInput.name = "columns"
    hideInput.value = columns;
    tempForm.appendChild(hideInput);

     var hideInput = document.createElement("input");
    hideInput.type = "hidden";
    hideInput.name = "geneList"
    hideInput.value = geneList;
    tempForm.appendChild(hideInput);

    $(tempForm).append($('#csrf').attr("value"));


    //open new window first
    openWindow(name);

    document.body.appendChild(tempForm);
    tempForm.submit();
    document.body.removeChild(tempForm);
}

function openWindow(name) {
    window.open('about:blank', name);
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
