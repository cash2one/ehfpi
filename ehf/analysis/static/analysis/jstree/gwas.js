/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {
    $("#jstree_gwas_div").bind("loaded.jstree", function (event, data) {
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

    $('#jstree_gwas_div').jstree({
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
            $('#jstree_gwas_div').jstree(true).search(v);
        }, 250);
    });

    $('#jstree_gwas_div').on("changed.jstree", function (e, data) {
        var pathogen = $("#jstree_gwas_div").jstree('get_selected');
        $('#jsTreeList').val(pathogen.join(','));
    });

    $('#resizable').resizable({
        minHeight: 400,
        minWidth: 600,
        autoHide: false
    });

    //qtip2
    $('#gwasTip').qtip({
        content: {
            title: 'GWAS Analysis',
            text: 'The guidance tree has four layers:\
            <ul>\
            <li>Kingdom</li>\
            <li>Family or Genus</li>\
            For virus is family, for bacteria and fungi is genus\
            <li>Species</li>\
            <li>Article</li>\
            first author-year-title\
            </ul>\
            the number mark at the end of each guidance item represents the total number of EHFPI accessions under this statistical category.'
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

function validEmpty() {
    var parms = $("#jstree_gwas_div").jstree('get_selected');
    if (($.trim(parms)).length > 0) {
        return true;
    } else {
        //popover hint
        $('#gwasAnalysis').popover({content: 'Please select pathogen!'});
        $('#gwasAnalysis').popover('show');
        setTimeout(function () {
            $('#gwasAnalysis').popover('destroy');
        }, 3000);
        return false;
    }

}