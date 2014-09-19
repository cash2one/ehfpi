// this js script get the Screen Scope div
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
                        <td class='advSearchLabel'>Screen Scope</td>\
                        <td >\
                            <div id='scopeParmDiv_scope_{{row}}'>\
                            <select id='scope_{{row}}' name ='scope_{{row}}' multiple class='form-control'>\
                            <option selected>all</option>\
                            {% for scopeItem in scope %}\
                                <option>{{ scopeItem }}</option>\
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


