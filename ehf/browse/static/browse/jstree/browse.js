/**
 * Created by jacky on 14-4-3.
 */
URL_PREFIX = '/ehfpi';
$(function () {

    $("#jstree_browse_div").bind("loaded.jstree", function (event, data) {
        data.instance.open_all();
    });
//    $("#jstree_browse_div").bind("loaded.jstree", function (event, data) {
//        /**
//         * Open nodes on load (until x'th level)
//         */
//        var depth = 2;
//        data.instance.get_container().find('li').each(function (i) {
//            if (data.instance.get_path($(this)).length <= depth) {
//                data.instance.open_node($(this));
//            }
//        });
//    });

    $('#jstree_browse_div').jstree({
        "types": {
            "default": {
                "draggable": false
            },

            "species": {
                "icon": "glyphicon glyphicon-leaf"
            },
            "year": {
                "icon": "glyphicon glyphicon-leaf"
            },
            "journal": {
                "icon": "glyphicon glyphicon-leaf"
            },
            "phenotype": {
                "icon": "glyphicon glyphicon-leaf"
            }
        },

        "search": {
            "fuzzy": false,
            "close_opened_onclear": true
        },

        "sort": function (a, b) {
            if (a.indexOf("_") > 0) {
                return this.get_text(a) > this.get_text(b) ? 1 : -1;
            }
        },

        "plugins": [ "search" , "wholerow", "checkbox", "types", "themes", "sort"]
    });

    var selectedNode = $('#selectedNode').text();
    if(selectedNode.length){
        var array1 = [];
        if(selectedNode.indexOf(';') > 0)
            array1 = selectedNode.split(';');
        else
            array1.push(selectedNode);

        for(var i=0;i<array1.length;i++){
            $('#jstree_browse_div').jstree('select_node', array1[i]);
        }
    }

    $('#jstree_browse_div').on('changed.jstree', function (e, data) {   // event
        var selected = $(this).jstree('get_selected');
        if (selected.length) {
            $.get(URL_PREFIX+"/browse/updateTable", {'selected': selected}, updateTable_evalCallbk);  //get search types from server
            $.get(URL_PREFIX+"/browse/updateBadge", {'selected': selected}, updateBadge_evalCallbk);  //get search types from server

        } else {  //the default page
            window.location.href = URL_PREFIX+'/browse/';
        }
    });

    var guideSelected = $('#guideSelected').text();
    if(guideSelected.length){
        var array2 = [];
        if(guideSelected.indexOf(';') > 0)
            array2 = guideSelected.split(';');
        else
            array2.push(guideSelected);

        for(var i=0;i<array2.length;i++){
            $('#jstree_browse_div').jstree('select_node', array2[i]);
        }
    }

    var to = false;
    $('#plugins4_q').keyup(function () {
        if (to) {
            clearTimeout(to);
        }
        to = setTimeout(function () {
            var v = $('#plugins4_q').val();
            $('#jstree_browse_div').jstree(true).search(v);
        }, 250);
    });

    $('#jstree_browse_div').on("changed.jstree", function (e, data) {
        console.log(data.selected);
    });

    //set default custom display columns in modal
    $("input[value='ehfpiAcc'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='ehfpiAcc'][id='checkboxColumn']").prop("disabled", "disabled");
    $("input[value='geneSymbol'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='species'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='title'][id='checkboxColumn']").prop("checked", "true");
    $("input[value='phenotype'][id='checkboxColumn']").prop("checked", "true");

    //set all columns for download
    $("input[id='checkboxDownload']").prop("checked", "true");

    //$('#jstree_browse_div').jstree('select_node', '#year_2000');
    //$.jstree.reference('#jstree_browse_div').select_node('#year_2000');
    //$('#jstree_browse_div').jstree(true).select_node('#year_2000');

    $('#resizable').resizable({
        maxHeight: 1000,
        maxWidth: 450,
        minHeight: 600,
        minWidth: 200
    });

    //guide accordion
    $('#accordion').accordion();

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

     //qtip2
    $('#browseAnalysisTip').qtip({
        content: {
            title:'Browse Result Operation',
            text:'You can do following operations:\
                    <ul>\
                        <li>Filter results</li>\
                        Filter results based on taxonomy, publication yeay, journal and phenotype, <span style="color:red;">the number on the right indicates \
                        the ehfpi entry number</span>. The panel is resizable.\
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

//ajax callback function for update table
function updateTable_evalCallbk(data) {
    document.getElementById('tabledivWrapper').innerHTML = data;  // we separate because paginate is uncontrollable
}

function updateBadge_evalCallbk(data) {
    eval(data);

}

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

//number of selected row
selectedNumber = 0;

//the go button
function performFunction(item) {

    //first check is there any data selected
    if (selectedNumber > 0) {
        //check the state of select
        var functionType = item;
        if (functionType == "download") {  //download data
            $('#downloadModal').modal('show');
            // now jump to modal

        } else if (functionType == "gea") {
            var type;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows

                selected = $('#jstree_browse_div').jstree('get_selected');
                if (selected.length) {
                    type = "allPage";
                } else {
                    type = "all";  //the default state, no tree item selected, yet all data is included
                }
            } else {  //only current page
                type = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });

            }
            $.get(URL_PREFIX+"/browse/gea", {'type': type, 'selected': selected}, gea_evalCallbk);
        }
        else if (functionType == "pip") {
            var type;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows

                selected = $('#jstree_browse_div').jstree('get_selected');
                if (selected.length) {
                    type = "allPage";
                } else {
                    type = "all";  //the default state, no tree item selected, yet all data is included
                }
            } else {  //only current page
                type = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });

            }
            window.open(URL_PREFIX+'/browse/pip?selected=' + selected + '&type=' + type);

        } else {//network
            var type;
            var selected;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows

                selected = $('#jstree_browse_div').jstree('get_selected');
                if (selected.length) {
                    type = "allPage";
                } else {
                    type = "all";  //the default state, no tree item selected, yet all data is included
                }
            } else {  //only current page
                type = "currentPage";
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });

            }
            window.open(URL_PREFIX+'/browse/network?selected=' + selected + '&type=' + type);
        }


    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
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

            selected = $('#jstree_browse_div').jstree('get_selected');
            if (selected.length) {
                type = "allPage";
            } else {
                type = "all";  //the default state, no tree item selected, yet all data is included
            }
        } else {  //only current page
            type = "currentPage";
            selected = new Array();
            $("input[name='tableRowCheckBox']").each(function () {
                if ($(this).prop("checked")) {
                    selected.push($(this).val());
                }
            });
        }

        //$.get("/browse/download", {'selectcolumn': selectcolumn, 'type': type, 'selected': selected}, download_evalCallbk);  //get search types from server
        $.fileDownload(URL_PREFIX+'/browse/download?selectcolumn=' + selectcolumn + '&type=' + type + '&selected=' + selected)
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

//gea callback function
function gea_evalCallbk(data) {  //data is the gene list
    if (data.length > 0) {
        //default go analysis
        var geneArary = data.split(",")
        if (geneArary.length <= 400) {
            window.open("http://david.abcc.ncifcrf.gov/api.jsp?type=GENE_SYMBOL&ids=" + data + "&tool=summary", "_blank");
        } else {
            $('#geaFunc').popover({content: 'gene number exceeds DAVID limitations, at most 400 genes,' + geneArary.length + ' genes provided'});
            $('#geaFunc').popover('show');
            setTimeout(function () {
                $('#geaFunc').popover('destroy');
            }, 3000);
        }

    }
}


columns = new Array();
//custom change columns, at most 8 columns, ehfpiAcc is default selected
function changeColumns(item) {
    columns.length = 0; //empty the array
    $("input[id='checkboxColumn']").each(function () {
        if ($(this).prop("checked")) {
            columns.push($(this).val());
        }
    });
    var selected = $('#jstree_browse_div').jstree('get_selected');
    $.get(URL_PREFIX+"/browse/updateTable", {'selected': selected,'columns':columns}, updateTable_evalCallbk);  //get search types from server
}