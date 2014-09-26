/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {
    $("#jstree_gea_div").bind("loaded.jstree", function (event, data) {
        /**
         * Open nodes on load (until x'th level)
         */
        data.instance.open_all();


//        var depth = 2;
//        data.instance.get_container().find('li').each(function (i) {
//            if (data.instance.get_path($(this)).length <= depth) {
//                data.instance.open_node($(this));
//            }
//        });
    });

    $('#jstree_gea_div').jstree({
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
                'valid_children': [ 'article' ],
                "icon": "glyphicon glyphicon-leaf"
            },
            "article": {
                'valid_children': [ 'none' ],
                "icon": "glyphicon glyphicon-flash"
            }
        },

        "search": {
            "fuzzy": false,
            "close_opened_onclear": true
        },

        "plugins": [ "search" , "wholerow", "checkbox", "types", "sort", "themes"]
    });

    var to = false;
    $('#plugins4_q').keyup(function () {
        if (to) {
            clearTimeout(to);
        }
        to = setTimeout(function () {
            var v = $('#plugins4_q').val();
            $('#jstree_gea_div').jstree(true).search(v);
        }, 250);
    });

    $('#jstree_gea_div').on("changed.jstree", function (e, data) {
        console.log(data.selected);
    });

    $('#resizable').resizable({
        minHeight: 400,
        minWidth: 600,
        autoHide: false
    });

    //qtip2
    $('#geaTip').qtip({
        content: {
            title: 'GEA Analysis',
            text: 'The guidance tree has four layers:\
            <ul>\
            <li>Kingdom</li>\
            <li>Family or Genus</li>\
            For virus is family, for bacteria and fungi is genus\
            <li>Species</li>\
            <li>Article</li>\
            first author-year-title\
            </ul>\
            the number mark at the end of each guidance item represents the total number of EHFPI accessions under this statistical category.<br/>\
            Select nodes and choose a analysis type, you may need to allow popup window!)'
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

// ajax request to get heatmap
function geaAnalysis() {
    // get select value
    var pathogen = $("#jstree_gea_div").jstree('get_selected');

    if (pathogen.length) {
        var analysisType = $("#analysisType").val();
        if (analysisType == "none") {
            //popover hint
            $('#doAnalysis').popover({content: 'please select a analysis type!'});
            $('#doAnalysis').popover('show');
            setTimeout(function () {
                $('#doAnalysis').popover('destroy');
            }, 3000);

        } else if (analysisType == "david") {
            //            if (geneArary.length <= 400) {
//                window.open("http://david.abcc.ncifcrf.gov/api.jsp?type=GENE_SYMBOL&ids=" + data + "&tool=summary", "_blank");
//            } else {
//                //popover hint
//                $('#doAnalysis').popover({content: 'gene number exceeds DAVID limitations, at most 400 genes, ' + geneArary.length + ' genes provided'});
//                $('#doAnalysis').popover('show');
//                setTimeout(function () {
//                    $('#doAnalysis').popover('destroy');
//                }, 3000);
//            }

            //20140925: we downloaded the knowledge base from DAVID, and provide a in-house result page for DAVID pathway and GO information.
            // For more information, you can still use the API provided by DAVID
            window.open(URL_PREFIX + "/analysis/gea/davidResult?pathogen="+pathogen, "_blank");  //open in a new window, pathogen list is short enough, otherwise we should use post




        } else {  //others, get geneList first, then display the modal
            $.get(URL_PREFIX + "/analysis/gea/getGeneList", {'pathogen': pathogen}, evalCallbk);  //get search types from server

        }

    } else {
        //popover hint
        $('#doAnalysis').popover({content: 'please choose pathogen'});
        $('#doAnalysis').popover('show');
        setTimeout(function () {
            $('#doAnalysis').popover('destroy');
        }, 3000);
    }
}

function evalCallbk(data) {  //data is the gene list
    if (data.length > 0) {
        var analysisType = $("#analysisType").val();

        if (analysisType == "others") {
            //Others
            $('#geaGeneList').text(data);
            $('#myModal').modal('show');
        }
        else {

        }
    } else {
        //popover hint
        $('#doAnalysis').popover({content: 'No gene found!'});
        $('#doAnalysis').popover('show');
        setTimeout(function () {
            $('#doAnalysis').popover('destroy');
        }, 3000);
    }
}

function evalCallbk_reactome(data) {
    var win = window.open('about:blank', URL_PREFIX + '/analysis/reactome/');
    with (win.document) {
        open();
        write(data);
        close();
    }
}