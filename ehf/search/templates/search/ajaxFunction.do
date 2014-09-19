// this js script get the EHF Function div for advanced search

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
                        <td class='advSearchLabel'>Phenotype</td>\
                        <td >\
                            <div id='functionParmDiv_function_{{row}}'>\
                            <select id='function_{{row}}' name='function_{{row}}' multiple class='form-control'>\
                            <option selected>all</option>\
                            {% for funcitonItem in function %}\
                                <option>{{ funcitonItem }}</option>\
                            {% endfor %}\
                                </select>\
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


