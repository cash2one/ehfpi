/**
 * Created by jacky on 14-3-24.
 */
$(function () {
    $("#jstree_network_div").bind("loaded.jstree", function (event, data) {
        data.instance.open_all();
    });

    $('#jstree_network_div').jstree({
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
            $('#jstree_network_div').jstree(true).search(v);
        }, 250);
    });

    $('#jstree_network_div').on("changed.jstree", function (e, data) {
        var pathogen = $("#jstree_network_div").jstree('get_selected');
        $('#jsTreeList').val(pathogen.join(','));
    });

    $('#resizable').resizable({
        maxHeight: 800,
        maxWidth: 800,
        minHeight: 200,
        minWidth: 300,
        autoHide: false
    });

    //qtip2
    $('#networkTip').qtip({
        content: {
            title: 'Network Analysis',
            text: 'You can input genes in three ways:\
            <ul>\
            <li>Taxonomy tree</li>\
            <li>Input a gene list</li>\
            Gene Symbol separated by comma, or one gene per line.\
            <li>Upload file</li>\
            Gene Symbol separated by comma, or one gene per line.\
            </ul>\
            Note it\'s not encouraged to submit too many genes!'
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

    //display file name
    $('#id_file').change(function () {
        var file_name = $("#id_file").val();

        $("#files").text(file_name);
        if (this.files && this.files.length) { //If this condition passes, you can get file size
            var file = this.files[0],
                fileSize = file.size || file.fileSize || 0;

            if (fileSize > 1024 * 1024 * 5) {  //5M max
                $("#files").text('');   //remove hint text
                $("#id_file").val('');  //cancel binding!!
                //popover hint
                $('#fileinput').popover({content: 'File too large(' + (fileSize / (1024 * 1024)).toFixed(1) + 'MB), maximum 5MB allowed!'});
                $('#fileinput').popover('show');
                setTimeout(function () {
                    $('#fileinput').popover('destroy');
                }, 3000);
            }
            else {
                $("#files").text(file_name + "(" + (fileSize / 1024).toFixed(1) + "KB)");
            }
        }
    });

});

function validEmpty() {
    var parms = $("#jstree_network_div").jstree('get_selected') + $('#id_geneList').val() + $('#id_file').val();
    if (($.trim(parms)).length > 0) {
        return true;
    } else {
        //popover hint
        $('#submitAll').popover({content: 'Please provide gene list!'});
        $('#submitAll').popover('show');
        setTimeout(function () {
            $('#submitAll').popover('destroy');
        }, 3000);
        return false;
    }

}