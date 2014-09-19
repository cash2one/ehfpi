/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {

    $("#accordion").accordion({
        heightStyle: "content"
    });

    $("#jstree_vtp_div").bind("loaded.jstree", function (event, data) {
        data.instance.open_all();
    });

    $('#jstree_vtp_div').jstree({
        "types": {
            "default": {
                "draggable": false
            },
            "kingdom": {
                "valid_children": [ "family", "genus" ]
            },
            "family": {
                "valid_children": [ "species" ]
            },
            "genus": {
                "valid_children": [ "species" ]
            },
            "species": {
                'valid_children': [ 'none' ],
                "icon": "glyphicon glyphicon-leaf"
            }
        },

        "search": {
            "fuzzy": false,
            "close_opened_onclear": true
        },

        "plugins": [ "search" , "wholerow", "checkbox", "types", "sort", "themes"]
    });

    var to = false;
    $('#vtp_plugins4_q').keyup(function () {
        if (to) {
            clearTimeout(to);
        }
        to = setTimeout(function () {
            var v = $('#vtp_plugins4_q').val();
            $('#jstree_vtp_div').jstree(true).search(v);
        }, 250);
    });

    $('#jstree_vtp_div').on("changed.jstree", function (e, data) {
        console.log(data.selected);
    });

    $('#resizable').resizable({
        maxHeight: 600,
        maxWidth: 500,
        minHeight: 300,
        minWidth: 200,
        autoHide: false
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

    //qtip2
    $('#vtpAnalysisTip').qtip({
        content: {
            title: 'PIP Analysis',
            text: 'You can do following operations:\
                    <ul>\
                        <li>download data</li>\
                        Select all or part of the results, and click "Download" button.\
                        <li>GEA analysis</li>\
                        Perform gene enrichment analysis using DAVID.\
                        <li>network analysis</li>\
                        The interaction network between gene and pathogen.\
                        <li>PPI network</li>\
                        Protein-protein interaction network.\
                        <li>PPI network(STRING)</li>\
                        PPI network linking to STRING.\
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

function getVTP() {
    var geneList = $('#geneList').val().replace(/(^\s*)|(\s*$)/g, '');  //remove space
    var pathogen = $("#jstree_vtp_div").jstree('get_selected');
    if (geneList.length + pathogen.length > 0) {

        $.get(URL_PREFIX + "/analysis/pip", {'geneList': geneList, 'pathogen': pathogen}, evalCallbk);  //get search types from server
    } else {
        //popover hint
        $('#vtpAnalysis').popover({content: 'please provide genes'});
        $('#vtpAnalysis').popover('show');
        setTimeout(function () {
            $('#vtpAnalysis').popover('destroy');
        }, 3000);
    }

}

function evalCallbk(data) {  //data is the gene list
    document.open();
    document.write(data);
    document.close();
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

//advanced result page
function performFunction(item) {

    //first check is there any data selected
    //var selectedNumber = $('#selectNumber')
    if (selectedNumber > 0) {
        //check the state of select
        var functionType = item;
        if (functionType == "download") {  //download data
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
            $.fileDownload(URL_PREFIX + '/analysis/pip/download?selected=' + selected)
                .done(function () {
                })
                .fail(function () {
                    alert('File download failed!');
                });

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
            //default go analysis
            if (selected.length <= 400) {
                window.open("http://david.abcc.ncifcrf.gov/api.jsp?type=GENE_SYMBOL&ids=" + selected.join(',') + "&tool=summary", "_blank");
            } else {
                $('#geaFunc').popover({content: 'gene number exceeds DAVID limitations, at most 400 genes,' + selected.length + ' genes provided'});
                $('#geaFunc').popover('show');
                setTimeout(function () {
                    $('#geaFunc').popover('destroy');
                }, 3000);
            }
        } else if (functionType == 'network') {//network
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
            openPostWindow(URL_PREFIX + '/analysis/pip/network/', selected, URL_PREFIX + '/analysis/pip/network/');
            //window.open(URL_PREFIX+'/analysis/pip/network?selected=' + selected);
        } else if (functionType == 'ppi') {
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
            openPostWindow(URL_PREFIX + '/analysis/pip/ppi/', selected, URL_PREFIX + '/analysis/pip/ppi/');

        } else {  //ppi_string

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

