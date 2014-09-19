/**
 * Created by jacky on 14-3-10.
 */

$(document).ready(function () {

    geneInfo = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('gene'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/static/data/gene.json'

    });

    pathogenInfo = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('pathogen'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/static/data/pathogen.json'
    });


    publicationInfo = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('publication'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/static/data/publication.json'
    });

    accInfo = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('acc'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/static/data/acc.json'
    });


    geneInfo.initialize();
    pathogenInfo.initialize();
    publicationInfo.initialize();
    accInfo.initialize();

    $('#focusedInpu').typeahead({
            hint: true,
            highlight: true,
            minLength: 1
        },
        {
            name: 'gene',
            displayKey: 'gene',
            source: geneInfo.ttAdapter(),
            templates: {
                header: '<h4 class="search-type">[Gene]</h4>'
            }
        },
        {
            name: 'pathogen',
            displayKey: 'pathogen',
            source: pathogenInfo.ttAdapter(),
            templates: {
                header: '<h4 class="search-type">[Pathogen]</h4>'
            }
        },
        {
            name: 'publication',
            displayKey: 'publication',
            source: publicationInfo.ttAdapter(),
            templates: {
                header: '<h4 class="search-type">[publication]</h4>'
            }
        },
        {
            name: 'acc',
            displayKey: 'acc',
            source: accInfo.ttAdapter(),
            templates: {
                header: '<h4 class="search-type">[EHFPI Acc]</h4>'
            }
        });

    /*
     update the navbar status, based on the url pattern
     * */
    var position = window.location.pathname;
    var idx1 = position.indexOf('/', 1);
    if (idx1 < 0) {  // ehfpi
        $('#home').addClass('active');
    } else {
        var idx2 = position.indexOf('/',idx1+1);
        if(idx2 < 0){
            $('#home').addClass('active');  // ehfpi/
        }else{

            var posName = position.substr(idx1+1, idx2 - idx1-1);
            if (posName == 'rest') { //in download now
                $('#download').addClass('active');
            } else {
                $('#' + posName).addClass('active');
            }
        }
    }

    //change focusedInpu stype!!!
    $('#focusedInpu').css('vertical-align', 'inherit');

    //clear search using jquery-clearsearch
    $('input[name=query]').clearSearch();

    //qtip2
    $('#searchTip').qtip({
        content: {
            title:'Quick Search',
            text:'Quick search supports four types:\
                    <ul>\
                        <li>Gene/Gene Product</li>\
                        gene symbol, previous name, synonyms, entrez gene id, uniprot id and ensembl gene id.\
                        <li>Pathogen</li>\
                        pathogen full name, pathogen abbreviation, pathogen aliases and taxonomy information(strain, species, genus, family, group and kingdom).\
                        <li>Publication</li>\
                        PUBMED id, title, journal, author and year.\
                        <li>EHFPI Acc</li>\
                        identifier of EHFPI entry.\
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

})
;


//change tips and typeahead
function changeTips(searchType) {
    var textField = document.getElementById("focusedInpu");  // get select
    if (textField) {
        if (searchType == "all") {
            $(textField).attr("placeholder", "Search everything");
            $('#focusedInpu').typeahead('destroy');
            $('#focusedInpu').typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                },
                {
                    name: 'gene',
                    displayKey: 'gene',
                    source: geneInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[Gene]</h4>'
                    }
                },
                {
                    name: 'pathogen',
                    displayKey: 'pathogen',
                    source: pathogenInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[Pathogen]</h4>'
                    }
                },
                {
                    name: 'publication',
                    displayKey: 'publication',
                    source: publicationInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[publication]</h4>'
                    }
                },
                {
                    name: 'acc',
                    displayKey: 'acc',
                    source: accInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[EHFPI Acc]</h4>'
                    }
                });

        }
        else if (searchType == "gene") {
            $(textField).attr("placeholder", "Gene Symbol(preferred), Entrez Gene ID. e.g., cbx4 ");
            $('#focusedInpu').typeahead('destroy');
            $('#focusedInpu').typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                },
                {
                    name: 'gene',
                    displayKey: 'gene',
                    source: geneInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[Gene]</h4>'
                    }
                });
        }
        else if (searchType == "pathogen") {
            $(textField).attr("placeholder", "e.g., hcv ");
            $('#focusedInpu').typeahead('destroy');
            $('#focusedInpu').typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                },
                {
                    name: 'pathogen',
                    displayKey: 'pathogen',
                    source: pathogenInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[Pathogen]</h4>'
                    }
                });
        }
        else if (searchType == "publication") {
            $(textField).attr("placeholder", "Author, Journal, Title, Year. e.g., nature");
            $('#focusedInpu').typeahead('destroy');
            $('#focusedInpu').typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                },
                {
                    name: 'publication',
                    displayKey: 'publication',
                    source: publicationInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[publication]</h4>'
                    }
                });
        }
        else if (searchType == "ehfpiacc") {
            $(textField).attr("placeholder", "e.g., ehfpi00001");
            $('#focusedInpu').typeahead('destroy');
            $('#focusedInpu').typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                },
                {
                    name: 'acc',
                    displayKey: 'acc',
                    source: accInfo.ttAdapter(),
                    templates: {
                        header: '<h4 class="search-type">[EHFPI Acc]</h4>'
                    }
                });
        } else {
        }
    }
    //change focusedInpu stype!!!
    $('#focusedInpu').css('vertical-align', 'inherit');

    $('input[name=query]').clearSearch();
}



