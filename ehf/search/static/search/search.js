URL_PREFIX = '/ehfpi';
$(function () {
    //set default custom display columns in modal
    $("input[value='ehfpiAcc'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='ehfpiAcc'][id='checkboxColumn']").prop("disabled", "disabled");
    $("input[value='geneSymbol'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='targetOrganism'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='strain'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='title'][id='checkboxColumn']").prop("checked", "true");

    //set all columns for download
    $("input[id='checkboxDownload']").prop("checked", "true");

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

    //qtip2
    $('#searchAnalysisTip').qtip({
        content: {
            title: 'Search Result Operation',
            text: 'You can do following operations:\
                    <ul>\
                        <li>customize displayed columns </li>\
                        Click the "Custom Display Columns" button and select the filelds.\
                        <li>download data</li>\
                        Select all or part of the results, and click "download" button.\
                        <li>GEA analysis</li>\
                        Perform gene enrichment analysis.\
                        <li>network analysis</li>\
                        The interaction network between gene and pathogen.\
                        <li>PIP analysis</li>\
                        The pathogen interacting proteins of selected results.\
                    </ul>'
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

});

//custom display columns, from download page
function changeState(item) {
    $("input[name='checkboxColumn']").prop("checked", $(item).prop("checked"));
    $("input[value='ehfpiAcc'][id='checkboxColumn']").prop("checked", "true");
}

columns = new Array();
//custom change columns,ehfpiAcc is default selected
function changeColumns(item) {
    columns.length = 0; //empty the array
    $("input[id ='checkboxColumn']").each(function () {
        if ($(this).prop("checked")) {
            columns.push($(this).val());
        }
    });
    var query = $('#query').text();
    var searchType = $('#searchType').text();
    window.location.href = URL_PREFIX + '/search/quick?searchType=' + searchType + '&query=' + query + '&columns=' + columns;
    //$.get("/search/quick", {'searchType': searchType, 'query': query,'columns':columns}, gea_evalCallbk);
}

//since in the advanced search, change will pass different parms, so we need this function
function changeColumnsAdvanced(item) {
    columns.length = 0; //empty the array
    $("input[id='checkboxColumn']").each(function () {
        if ($(this).prop("checked")) {
            columns.push($(this).val());
        }
    });
    //parse url address, same in search change columns
    var url = window.location.search.substr(1);
    var urlList = url.split("&");
    var columnIn = 0;
    for (var i = 0; i < urlList.length; i++) {
        var index = urlList[i].indexOf('=');
        var myKey = urlList[i].substr(0, index);
        if (myKey == 'columns') {  //in the url
            urlList[i] = 'columns=' + columns;
            columnIn = 1;
            break;
        }
    }
    if (columnIn == 0) {
        url = window.location.search + '&columns=' + columns;
    } else {
        url = '?' + urlList.join("&");
    }

    //console.log(url);
    window.location.href = URL_PREFIX + '/search/advanced/' + url;

}

//since in the preview, change will pass different parms, so we need this function
function changeColumnsPreview(item) {
    columns.length = 0; //empty the array
    $("input[id='checkboxColumn']").each(function () {
        if ($(this).prop("checked")) {
            columns.push($(this).val());
        }
    });

    //parse url address, same in search change columns
    var url = window.location.search.substr(1);
    var urlList = url.split("&");
    var columnIn = 0;
    for (var i = 0; i < urlList.length; i++) {
        var index = urlList[i].indexOf('=');
        var myKey = urlList[i].substr(0, index);
        if (myKey == 'columns') {  //in the url
            urlList[i] = 'columns=' + columns;
            columnIn = 1;
            break;
        }
    }
    if (columnIn == 0) {
        url = window.location.search + '&columns=' + columns;
    } else {
        url = '?' + urlList.join("&");
    }

    window.location.href = URL_PREFIX + '/browse/previewResult/' + url;
}

//for heatmap analysis result display
function changeColumnsHeatmap(item) {
    columns.length = 0; //empty the array
    $("input[id='checkboxColumn']").each(function () {
        if ($(this).prop("checked")) {
            columns.push($(this).val());
        }
    });

    //parse url address, same in search change columns
    var url = window.location.search.substr(1);
    var urlList = url.split("&");
    var columnIn = 0;
    for (var i = 0; i < urlList.length; i++) {
        var index = urlList[i].indexOf('=');
        var myKey = urlList[i].substr(0, index);
        if (myKey == 'columns') {  //in the url
            urlList[i] = 'columns=' + columns;
            columnIn = 1;
            break;
        }
    }
    if (columnIn == 0) {
        url = window.location.search + '&columns=' + columns;
    } else {
        url = '?' + urlList.join("&");
    }

    window.location.href = URL_PREFIX + '/analysis/overlap/heatMapResult' + url;
}

//select rows of all pages, including those not displayed
//it seems that it is the same with selectCurrentPage, we will check the state of this checkbox
function selectAllPage(item) {
    $('#selectCurrentPage').prop("checked", $(item).prop("checked"));
    $("input[name='tableRowCheckBox']").prop("checked", $(item).prop("checked"));
    updateSelectNumber();
}

//select all rows of current page
function selectCurrentPage(item) {
    $("input[name='tableRowCheckBox']").prop("checked", $(item).prop("checked"));
    if ($(item).prop("checked") == false) {
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

//check if not all selected, just uncheck the selectCurrentPage and selectAllPageCheckbox
function stillSelectAll(item) {
    if ($(item).prop("checked") == false) {
        $('#selectCurrentPage').prop("checked", false);
        $('#selectAllPage').prop("checked", false);
    }
    updateSelectNumber();
}

//number of selected row
selectedNumber = 0;

//the go button
function performFunction(item) {

    //first check is there any data selected
    if (selectedNumber > 0) {
        var functionType = item;
        if (functionType == "download") {  //download data
            $('#downloadModal').modal('show');
            // now jump to modal

        } else if (functionType == "gea") {
            var type;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                type = "allPage";
                selected = new Array();
                selected.push($('#query').text());   //query
                selected.push($('#searchType').text());  //search type

            } else {  //only current page
                type = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });

            }
            $.get(URL_PREFIX + "/search/gea", {'type': type, 'selected': selected}, gea_evalCallbk);
        }
        else if (functionType == "pip") {
            var type;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                type = "allPage";
                selected = new Array();
                selected.push($('#query').text());   //query
                selected.push($('#searchType').text());  //search type

            } else {  //only current page
                type = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });

            }
            //window.location.href = '/search/vtp?selected=' + selected + '&type=' + type;
            window.open(URL_PREFIX + '/search/pip?selected=' + selected + '&type=' + type);

        } else {//network analysis
            var type;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                type = "allPage";
                selected = new Array();
                selected.push($('#query').text());   //query
                selected.push($('#searchType').text());  //search type

            } else {  //only current page
                type = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });

            }
            //here is a bit complicated. We use the following method:
            //1. pass the selected items to network function, it first get gene symbol just like vtp function
            //2. return the overlapNetwork templates
            //3. in the templates script call ajax to get needed data
            //4. change the map
            window.open(URL_PREFIX + '/search/network?selected=' + selected + '&type=' + type);
        }


    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
    }


}

//advanced result page
function performFunction_Advanced(item) {

    //first check is there any data selected
    //var selectedNumber = $('#selectNumber')
    if (selectedNumber > 0) {
        //check the state of select
        var functionType = item;
        if (functionType == "download") {  //download data
            $('#downloadModal').modal('show');
            // now jump to modal

        } else if (functionType == "gea") {
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = new Array();
                selected = $('#ids').text().split(',');

            } else {  //only current page
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
            }
            $.post(URL_PREFIX + "/search/geaAdvanced/", {'selected': selected}, gea_evalCallbk);
        }
        else if (functionType == "pip") {
            var queryType;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                queryType = "allPage";
                //selected = new Array();
                //selected = $('#ids').text().split(',');
                selected = location.search.substr(1);
                window.open(URL_PREFIX + '/search/pipAdvanced?' + selected + '&queryType=' + queryType);

            } else {  //only current page
                queryType = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
                window.open(URL_PREFIX + '/search/pipAdvanced?selected=' + selected + '&queryType=' + queryType);
            }


        } else {//network
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = new Array();
                selected = $('#ids').text().split(',');

            } else {  //only current page
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
            }
            //create a form here
//            var form = $('<form method="post" action="' + URL_PREFIX + '/search/networkAdvanced/">' +
//                '<input type="hidden" name="selected" value="' + selected + '"></form>');
//            $(form).submit();

            openPostWindow(URL_PREFIX + '/search/networkAdvanced/', selected, URL_PREFIX + '/search/networkAdvanced/');
            //window.open(URL_PREFIX+'/search/networkAdvanced?selected=' + selected);
        }


    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
    }


}

//heatmap result page
function performFunction_heatmap(item) {

    //first check is there any data selected
    //var selectedNumber = $('#selectNumber')
    if (selectedNumber > 0) {
        //check the state of select
        var functionType = item;
        if (functionType == "download") {  //download data
            $('#downloadModal').modal('show');
            // now jump to modal

        } else if (functionType == "gea") {
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = new Array();
                selected = $('#ids').text().split(',');

            } else {  //only current page
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
            }
            $.post(URL_PREFIX + "/search/geaAdvanced/", {'selected': selected}, gea_evalCallbk);
        }
        else if (functionType == "pip") {
            var queryType;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                queryType = "allPage";
                //selected = new Array();
                //selected = $('#ids').text().split(',');
                selected = location.search.substr(1);
                window.open(URL_PREFIX + '/search/pipHeatmap?' + selected + '&queryType=' + queryType);
            } else {  //only current page
                queryType = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
                window.open(URL_PREFIX + '/search/pipHeatmap?selected=' + selected + '&queryType=' + queryType);
            }


        } else {//network
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = new Array();
                selected = $('#ids').text().split(',');

            } else {  //only current page
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
            }
            //create a form here
//            var form = $('<form method="post" action="' + URL_PREFIX + '/search/networkAdvanced/">' +
//                '<input type="hidden" name="selected" value="' + selected + '"></form>');
//            $(form).submit();

            openPostWindow(URL_PREFIX + '/search/networkAdvanced/', selected, URL_PREFIX + '/search/networkAdvanced/');
            //window.open(URL_PREFIX+'/search/networkAdvanced?selected=' + selected);
        }


    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
    }


}

//preview result page
function performFunction_preview(item) {

    //first check is there any data selected
    //var selectedNumber = $('#selectNumber')
    if (selectedNumber > 0) {
        //check the state of select
        var functionType = item;
        if (functionType == "download") {  //download data
            $('#downloadModal').modal('show');
            // now jump to modal

        } else if (functionType == "gea") {
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = new Array();
                selected = $('#ids').text().split(',');

            } else {  //only current page
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
            }
            $.post(URL_PREFIX + "/search/geaAdvanced/", {'selected': selected}, gea_evalCallbk);
        }
        else if (functionType == "pip") {
            var queryType;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                queryType = "allPage";
                //selected = new Array();
                //selected = $('#ids').text().split(',');
                selected = location.search.substr(1);
                window.open(URL_PREFIX + '/search/pipPreview?' + selected + '&queryType=' + queryType);
            } else {  //only current page
                queryType = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
                window.open(URL_PREFIX + '/search/pipPreview?selected=' + selected + '&queryType=' + queryType);
            }


        } else {//network
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = new Array();
                selected = $('#ids').text().split(',');

            } else {  //only current page
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
            }
            //create a form here
//            var form = $('<form method="post" action="' + URL_PREFIX + '/search/networkAdvanced/">' +
//                '<input type="hidden" name="selected" value="' + selected + '"></form>');
//            $(form).submit();

            openPostWindow(URL_PREFIX + '/search/networkAdvanced/', selected, URL_PREFIX + '/search/networkAdvanced/');
            //window.open(URL_PREFIX+'/search/networkAdvanced?selected=' + selected);
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
function openPostWindow(url, data, name) {
    var tempForm = document.createElement("form");
    tempForm.id = "tempForm1";
    tempForm.method = "post";
    tempForm.action = url;
    tempForm.target = name;

    var hideInput = document.createElement("input");
    hideInput.type = "hidden";
    hideInput.name = "selected"
    hideInput.value = data;
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


//gea callback function
function gea_evalCallbk(data) {  //data is the gene list
    if (data.length > 0) {
        //default go analysis
        var geneArary = data.split(",")
        if (geneArary.length <= 400) {
            window.open("http://david.abcc.ncifcrf.gov/api.jsp?type=GENE_SYMBOL&ids=" + data + "&tool=summary", "_blank", 'fullscreen=1,toolbar=yes, menubar=yes, scrollbars=yes, resizable=yes,location=yes, status=yes');
        } else {
            $('#geaFunc').popover({content: 'gene number exceeds DAVID limitations, at most 400 genes,' + geneArary.length + ' genes provided'});
            $('#geaFunc').popover('show');
            setTimeout(function () {
                $('#geaFunc').popover('destroy');
            }, 3000);
        }

    }
}


function downloadData(item) {
    //get select columns
    var selectcolumn = new Array();
    $("input[id='checkboxDownload']").each(function () {
        if ($(this).prop("checked")) {
            selectcolumn.push($(this).val());
        }
    });
    if (selectcolumn.length) {  //at least one column

        var type;
        var selected;
        //get the selected items
        if ($('#selectAllPage').prop("checked")) {  //select all rows
            type = "allPage";
            selected = new Array();
            selected.push($('#query').text());   //query
            selected.push($('#searchType').text());  //search type

        } else {  //only current page
            type = "currentPage";
            selected = new Array();
            $("input[name='tableRowCheckBox']").each(function () {
                if ($(this).prop("checked")) {
                    selected.push($(this).val());
                }
            });
        }

        $.fileDownload(URL_PREFIX + '/search/download?selectcolumn=' + selectcolumn + '&type=' + type + '&selected=' + selected)
            .done(function () {
            })
            .fail(function () {
                alert('File download failed!');
            });
    }

}

function downloadDataAdvanced(item) {
    //get select columns
    var selectcolumn = new Array();
    $("input[id='checkboxDownload']").each(function () {
        if ($(this).prop("checked")) {
            selectcolumn.push($(this).val());
        }
    });
    if (selectcolumn.length) {  //at least one column
        var selected;
        //get the selected items
        if ($('#selectAllPage').prop("checked")) {  //select all rows
            selected = new Array();
            selected = $('#ids').text().split(',');

        } else {  //only current page
            selected = new Array();
            $("input[name='tableRowCheckBox']").each(function () {
                if ($(this).prop("checked")) {
                    selected.push($(this).val());
                }
            });
        }

        var csrf = $('#csrf').attr("value");
        var index = csrf.indexOf('value=');
        var index2 = csrf.lastIndexOf("'");
        var csrfmiddlewaretoken = csrf.substr(index+7,index2-index-7);

        $.fileDownload(URL_PREFIX + '/search/downloadAdvanced/',
            {
                httpMethod: "POST",
                data:{
                    selectcolumn:selectcolumn,
                    selected:selected,
                    csrfmiddlewaretoken:csrfmiddlewaretoken
                }
            })
            .done(function () {
            })
            .fail(function () {
                alert('File download failed!');
            });
    }

}

//download data callback function
function download_evalCallbk(data) {

}