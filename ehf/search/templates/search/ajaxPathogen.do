// this js script get the Pathogen div

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
                        <td class='advSearchLabel'>Kingdom</td>\
                        <td >\
                            <div id='pathogenParmDiv_kingdom_{{row}}'>\
                            <select id='pathogen_kingdom_{{row}}' name ='pathogen_kingdom_{{row}}' multiple class='form-control' onchange='changeSelect(this)'>\
                            <option selected>all</option>\
                            {% for kingdomItem in kingdom %}\
                                <option>{{ kingdomItem }}</option>\
                            {% endfor %}\
                                </select>\
                            </div>\
                        </td>\
                        <td class='advSearchLabel'>Species</td>\
                        <td >\
                            <div id='pathogenParmDiv_species_{{row}}'>\
                            <select id='pathogen_species_{{row}}' name ='pathogen_species_{{row}}' multiple class='form-control'>\
                            <option selected>all</option>\
                            {% for speciesItem in species %}\
                                <option>{{ speciesItem }}</option>\
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
