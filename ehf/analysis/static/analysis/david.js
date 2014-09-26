/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {
    //set the bar width
    var bp = $('#bp').text();
    var cc = $('#cc').text();
    var mf = $('#mf').text();
    var BBID = $('#BBID').text();
    var KEGG = $('#KEGG').text();
    var PANTHER = $('#PANTHER').text();
    var REACTOME = $('#REACTOME').text();
    var maxGO = $('#maxGO').text();
    var maxPathway = $('#maxPathway').text();
    var geneList = $('#geneList').text();

    $('#bpImage').attr('width', bp * 200 / maxGO);
    $('#ccImage').attr('width', cc * 200 / maxGO);
    $('#mfImage').attr('width', mf * 200 / maxGO);

    $('#BBIDImage').attr('width', BBID * 200 / maxPathway);
    $('#KEGGImage').attr('width', KEGG * 200 / maxPathway);
    $('#PANTHERImage').attr('width', PANTHER * 200 / maxPathway);
    $('#REACTOMEImage').attr('width', REACTOME * 200 / maxPathway);

    $('#davidLink').attr('href', "http://david.abcc.ncifcrf.gov/api.jsp?type=GENE_SYMBOL&ids=" + geneList + "&tool=summary")

});

function getAnnotationReport(type) {
    var geneList = $('#geneList').text();
    var currAddr = location.href;
    window.open(currAddr + "&type=" + type, "_blank");
}

//download the annotation report
function downAnnotationReport() {
    var currAddr = location.search;
    $.fileDownload(URL_PREFIX + '/analysis/gea/downAnnotationReport' + currAddr)
        .done(function () {
        })
        .fail(function () {
            alert('File download failed!');
        });
}

