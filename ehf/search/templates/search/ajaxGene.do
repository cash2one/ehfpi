// this js script get the Gene div for advanced search

clearTimeout(loadingTimeout)
loadingTimeout = null
showProcessingParmDiv({{ row }},"");

var text = "<fieldset>\
    <table id='myParmTable_{{row}}' class='advSearchTable'>\
        <tbody id='myParmTbody_{{row}}'>\
        <tr>\
            <td>\
                <table class='advSearchTable'>\
                    <tbody>\
                    <tr>\
                        <td class='advSearchLabel'>ID(s)</td>\
                        <td nowrap='' style='text-align: left;'>\
                            <div id='geneParmDiv_geneList_{{ row }}'><textarea class='advSearchInput resizable'\
                                                                             type='text' name='geneList_{{row}}'\
                                                                             id='gene_{{row}}' wrap='physical'\
                                                                             value=''\
                                                                             onclick='resizeMe(0); this.focus();'></textarea>\
                            </div>\
                        </td>\
                    </tr>\
                    </tbody>\
                </table>\
            </td>\
        </tr>\
        </tbody>\
    </table>\
</fieldset>\
";
// change the html
var aDiv = document.getElementById("smartParmDiv_" + {{ row }});
aDiv.innerHTML = text;


