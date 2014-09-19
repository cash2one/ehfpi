// this js script get the Publication div
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
                        <td class='advSearchLabel'>Author</td>\
                        <td class='selectTd'>\
                            <div id='publicationParmDiv_title_{{row}}'>\
                            <select id='publication_title_{{row}}' name ='publication_title_{{row}}' multiple class='form-control'>\
                            <option selected>all</option>\
                            {% for titleItem in title %}\
                                <option>{{ titleItem }}</option>\
                            {% endfor %}\
                                </select>\
                            </div>\
                        </td>\
                        <td class='advSearchLabel'>Journal</td>\
                        <td class='selectTd'>\
                            <div id='publicationParmDiv_journal_{{row}}'>\
                            <select id = 'publication_journal_{{row}}' name = 'publication_journal_{{row}}'  multiple class='form-control'>\
                            <option selected>all</option>\
                            {% for journalItem in journal %}\
                                <option>{{ journalItem }}</option>\
                            {% endfor %}\
                                </select>\
                            </div>\
                        </td>\
                        <td class='advSearchLabel'>Year</td>\
                        <td class='selectTd'>\
                            <div id='publicationParmDiv_year_{{row}}'>\
                            <select id = 'publication_year_{{row}}' name = 'publication_year_{{row}}'  multiple class='form-control'>\
                            <option selected>all</option>\
                            {% for yearItem in year %}\
                                <option>{{ yearItem }}</option>\
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


