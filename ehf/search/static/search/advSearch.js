var searchtypes;
var type2st;
var prompts;
var prompt_tips;
var prompt_descs;
var smart_isIE = (navigator.appName == "Microsoft Internet Explorer");
var smart_isIEMac = (smart_isIE && navigator.userAgent.indexOf("Mac") != -1);

URL_PREFIX = '/ehfpi';
//used
function getSearchType(rownum) {
    var aRow = document.getElementById("smartHeadTr_" + rownum);
    if (aRow) 
    {
        var tdElem = document.createElement("td");
        $(tdElem).css({"width": "100px"});
        tdElem.innerHTML = getSearchTypeHtml(rownum);
        aRow.appendChild(tdElem);

        var tdElem = document.createElement("td");
        $(tdElem).attr("id", "smartTip_" + rownum);
        $(tdElem).css({"font-weight": "normal"});
        aRow.appendChild(tdElem);

        var tdElem = document.createElement("td");
        $(tdElem).css({"width": "10px"});
        btnNode = document.createElement("img");
        if (smart_isIE) 
        {
            btnNode.src = "/static/search/images/minus.png";
            btnNode.id = "clearSmartRow_" + rowId;
            btnNode.setAttribute("class", "clearSmartRow");
            btnNode.attachEvent("onclick", clearSmartRow);
        } 
        else 
        {
            btnNode.setAttribute("src", "/static/search/images/minus.png");
            btnNode.setAttribute("id", "clearSmartRow_" + rowId);
            btnNode.setAttribute("class", "clearSmartRow");
            btnNode.setAttribute("onClick", "clearSmartRow(event);");
        }
        tdElem.appendChild(btnNode);
        aRow.appendChild(tdElem);
    } 
    else 
    {
        alert("couldnt find row: " + rownum);
    }
}

//used
function getSearchTypeHtml(rownum) {
    var output = new Array();
    output.push("<select class='selectsmall' name='smartSearchSubtype_");
    output.push(rownum);
    output.push("' id='smartSearchSubtype_");
    output.push(rownum);
    output.push("' onChange='addParms(");
    output.push(rownum);
    output.push(", this.value);'>");
    output.push("<option value='' selected>Choose a Query Type:</option>");
    for (n in searchtypes) 
    {
        output.push("<option value='");
        output.push(type2st[searchtypes[n]]);
        output.push("' onmouseover=\"smartTip('");
        output.push(prompt_tips[type2st[searchtypes[n]]]);
        output.push("', '");
        output.push(rownum);
        output.push("');\" onmouseout=\"smartUnTip('");
        output.push(rownum);
        output.push("');\">&nbsp;&nbsp;&nbsp;");
        output.push(prompts[type2st[searchtypes[n]]]);
        output.push("</option>\n");
    }
    output.push("</select>");
    return output.join("");
}

//used
function setSelectedList(list, valueIn) {
    if (valueIn <= '') 
    {
        return;
    }
    if (list.options[0]) 
    {
        for (var i = 0; i < list.options.length; i++)
        {
            if (list.options[i].value == valueIn) 
            {
                list.options[i].selected = true;
                return;
            }
        }
        $(list).append('<optgroup label="Current Critera"><option onmouseout="smartUnTip(\'0\');" selected="selected" onmouseover="smartTip(\'Current option\', \'0\');" value="' + valueIn + '">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Current Criteria (' + valueIn + ')</option></optgroup>');
    }
}

//used
function evalCallbk(data) {
    // why eval to execute the js code, because in the callback function we need to get the rowid, so not choose html
    eval(data);
}

//used
function addParmsPlaceholder(row) {
    var aDiv = document.getElementById("smartParmDiv_" + row);
    if (aDiv) 
    {
        aDiv.innerHTML = '';
        var inputNode = document.createElement("INPUT");
        if (smart_isIE) 
        {
            inputNode.type = "hidden";
            inputNode.name = "t_" + row;
            inputNode.id = "t_" + row;
        } 
        else 
        {
            inputNode.setAttribute("type", "hidden");
            inputNode.setAttribute("name", "t_" + row);
            inputNode.setAttribute("id", "t_" + row);
        }
        aDiv.appendChild(inputNode);
        inputNode = document.createElement("INPUT");
        if (smart_isIE) 
        {
            inputNode.type = "hidden";
            inputNode.name = "n_" + row;
            inputNode.id = "n_" + row;
        } 
        else 
        {
            inputNode.setAttribute("type", "hidden");
            inputNode.setAttribute("name", "n_" + row);
            inputNode.setAttribute("id", "n_" + row);
        }
        aDiv.appendChild(inputNode);
//        inputNode = document.createElement("INPUT");
//        if (smart_isIE)
//        {
//            inputNode.type = "text";
//            inputNode.disabled = "true";
//            inputNode.name = "nodeDesc_" + row;
//            inputNode.id = "nodeDesc_" + row;
//        }
//        else
//        {
//            inputNode.setAttribute("type", "text");
//            inputNode.setAttribute("disabled", "true");
//            inputNode.setAttribute("name", "nodeDesc_" + row);
//            inputNode.setAttribute("id", "nodeDesc_" + row);
//        }
        inputNode = document.createElement("div");
        inputNode.innerHTML = 'choose a query type from the select above';
        aDiv.appendChild(inputNode);
        aDiv.setAttribute("class", "selectsmall");
        //$("#evalSmartRow_" + row).attr("disabled", true);
    } 
    else 
    {
        alert("couldnt find div: " + row);
    }
}

//used
function showProcessingParmDiv(row, inner) {
    var aDiv = document.getElementById("smartParmLoadingDiv_" + row);
    if (aDiv) 
    {
        if (inner) 
        {
            aDiv.innerHTML = inner;
            aDiv.setAttribute("class", "selectsmall");
        } 
        else 
        {
            aDiv.innerHTML = "&nbsp;";
        }
    } 
    else 
    {
        alert("couldnt find div: " + row);
    }
}
var loadingTimeout = null;
var currentrowid = null

//this function generate form based on the search type choice
function addParms(row, searchType) 
{
    enableStartOver();
    var aSt = document.getElementById("smartSearchSubtype_" + row);
    if (aSt) 
    {
        var i = aSt.selectedIndex;
        if (aSt.options[i].value.length == 0)  //the first line
        {
            aSt.options[i + 1].selected = true;
            searchType = aSt.options[i + 1].value;
        }
    }
    //clearResults(row); not needed in out project
    currentrowid = row;
    loadingTimeout = setTimeout('showProcessingParmDiv(' + row + ', "<h3><i>Loading...</i></h3>")', 20);
    $.get(URL_PREFIX+"/search/advanced/smartSubqueryParms", {'r': row,'st': searchType}, evalCallbk);  //get search types from server
    var aDesc = document.getElementById("smartSearchDesc_" + row);
    aDesc.innerHTML = prompt_descs[searchType];
    // $("#evalSmartRow_" + row).removeAttr("disabled"); not needed in out project
}

//this function is for pathogen advanced search, when kingdom is selected, species is displayed accordingly
function changeSelect(str)
{
    var parentId = $(str).parent().attr("id");
    var currRow = parentId.substr(parentId.lastIndexOf('_')+1);
    var selectVal = $(str).val();
    var selectStr = "";
    // we can use json, but cat the string is more convenient

    for (var i = 0; i < selectVal.length - 1; i++)
        selectStr = selectStr + selectVal[i] + ",";
    selectStr = selectStr + selectVal[selectVal.length - 1]

    $.get(URL_PREFIX+"/search/advanced/getSpecies", {'r': currRow, 'stv': selectStr}, evalCallbk);  //get search types from server

}

//used
var rowId = 0;
function smartRow() {
    newRowId = "smartTr_" + rowId;
    var tbodyElem = document.getElementById("myTbody1");
    var mainTrElem, mainTdElem, trElem, tdElem, txtNode, divNode, btnNode, imgNode, linkNode, iframeNode, newRowId, hrNode;
    var sAttr = (window.clientInformation) ? "className" : "class";
    var r = tbodyElem.rows.length;
    mainTrElem = tbodyElem.insertRow(tbodyElem.rows.length);
    $(mainTrElem).attr("id", newRowId);
    mainTdElem = mainTrElem.insertCell(mainTrElem.cells.length);
    if (tbodyElem.rows.length > 1) {  //more than one condition, add AND or OR based on the value in smart comparator div
        var spacerDiv = document.createElement('div');
        $(spacerDiv).css({"text-align": "left", "padding-bottom": "4px"});
        var spacerH1 = document.createElement('h1');
        $(spacerH1).attr("class", "smart_spacer");
        $(spacerH1).css({"font-size": "16px", "color": "#6493c2"});
        var comparator = document.getElementById("smartComparator");
        var selectedComparator = comparator.value;
        spacerH1.innerHTML = selectedComparator.toUpperCase();
        spacerDiv.appendChild(spacerH1);
        mainTdElem.appendChild(spacerDiv);
    }
    var headerDiv = document.createElement('div');
    $(headerDiv).attr("class", "b_head3");
    $(headerDiv).css({"padding-top": "3px"});
    var newTable = document.createElement('table');
    $(newTable).attr("id", "smartContainerTable_" + rowId);
    $(newTable).attr("class", "plain");
    newRow = newTable.insertRow(0);
    $(newRow).attr("id", "smartHeadTr_" + rowId);
    headerDiv.appendChild(newTable);
    mainTdElem.appendChild(headerDiv);
    getSearchType(rowId);  //insert the select section
    var bodyDiv = document.createElement('div');
    $(bodyDiv).attr("class", "w_body3");
    var bodyContentDiv = document.createElement('div');
    $(bodyContentDiv).attr("class", "box_contentWrapper");
    var bodyTable = document.createElement('table');
    $(bodyTable).attr("id", "smartBodyTable_" + rowId);
    $(bodyTable).attr("class", "plain");
    trElem = bodyTable.insertRow(bodyTable.rows.length);
    tdElem = trElem.insertCell(trElem.cells.length);  //this td item is the promots description defined in advancedSearch.html, you can change it
    $(tdElem).attr("id", "smartSearchDesc_" + rowId);
    $(tdElem).each(function () {
        this.colSpan = 4;
    });
    $(tdElem).css({"font-style": "oblique"});
    trElem = bodyTable.insertRow(bodyTable.rows.length);
    $(trElem).attr("id", "search_" + newRowId);

    tdElem = trElem.insertCell(trElem.cells.length);
    $(tdElem).attr("class", "smartParmLoading");
    divProcNode = document.createElement("div");   //the loading promot, like LOADING ...
    $(divProcNode).attr("id", "smartParmLoadingDiv_" + rowId);
    tdElem.appendChild(divProcNode);

    tdElem = trElem.insertCell(trElem.cells.length);   //the main content part for each search type
    $(tdElem).attr("class", "smartMain");
    divNode = document.createElement("div");
    $(divNode).attr("id", "smartParmDiv_" + rowId);
    tdElem.appendChild(divNode);

    bodyContentDiv.appendChild(bodyTable);
    bodyDiv.appendChild(bodyContentDiv);
    mainTdElem.appendChild(bodyDiv);
    addParmsPlaceholder(rowId);   //add input field in the smartParmDiv div
    // addResult(rowId, ' '); result count div is removed
    var footerDiv = document.createElement('div');
    $(footerDiv).attr("class", "w_foot3");
    $(footerDiv).css({"height": "10px"});
    mainTdElem.appendChild(footerDiv);
    toggleClearButton();   //display the clear pic or not based on the smartrow number
    if (tbodyElem.rows.length == 1)  //more than one row then display the AND and OR
        $('select#smartComparator').attr('disabled', "disabled")
    else {
        $('select#smartComparator').removeAttr('disabled');
    }
    rowId++;
}

//used
function getRowFromEvent(evt) {
    var rownum;
    evt = (evt) ? evt : ((window.event) ? window.event : "");
    if (evt) {
        var elem;
        if (evt.target) {
            if (evt.currentTarget && (evt.currentTarget != evt.target)) {
                elem = evt.currentTarget;
            } else {
                elem = evt.target;
            }
        } else {
            elem = evt.srcElement;
        }
        if (elem.id) 
        {
            pos = elem.id.lastIndexOf('_');
            if (pos > 1) 
            {
                rownum = elem.id.substr(pos + 1);
            } 
            else 
            {
                alert("problem in getRowFromEvent: " + elem);
            }
        }
    }
    return rownum;
}

//used
function toggleClearButton() {
    var numOfSmartRows = $("img.clearSmartRow").size();
    if (numOfSmartRows == 1) {
        $("img.clearSmartRow").hide();
    } else {
        $("img.clearSmartRow").show();
    }
}

//used
function clearSmartRow(evt) {
    var rownum = getRowFromEvent(evt);
    // $.post("/pdb/search/clearSmartRow.do", {'r': rownum});  //ajax in server part, modify the search params
    var trId = "smartTr_" + rownum;
    var trIdSearch = "search_" + trId;
    var rowSpacer = trId + "spacer";
    var node = document.getElementById(trId);
    var nodeSearch = document.getElementById(trIdSearch);
    if (node) 
    {
        node.parentNode.removeChild(node);
        nodeSearch.parentNode.removeChild(nodeSearch);
    }
    node = document.getElementById(rowSpacer);
    if (node) 
    {
        node.parentNode.removeChild(node);
    }
    var tbody1 = document.getElementById("myTbody1");
    if (tbody1.rows.length > 0) 
    {
        var anId = tbody1.rows[0].id;
        if (anId.indexOf("spacer") > 0) 
        {
            tbody1.removeChild(tbody1.rows[0]);
        }
        if (tbody1.rows.length == 1) {
            $('select#smartComparator').attr('disabled', "disabled");
        }
    }
    if (tbody1.rows.length == 0) 
    {
        rowId = 0;
        smartRow();
    }
    var oldSpacer = $("#myTbody1").find("tr:first");
    var oldSpacerH1 = $(oldSpacer).find("h1.smart_spacer");
    $(oldSpacerH1).hide();
    toggleClearButton();
    return true;
}

//used
function clearSmart() { //clear all parameter
    $("#startOver").attr("disabled", "disabled");
    $("#doSearch").attr("disabled", "disabled");   //this line is also needed, when ther is no params, we should not submit the query
    //$.post("/pdb/search/clearSmartRow.do", {'r': 'all'});   //pass all row number
    if (document.createElement && !smart_isIEMac) 
    {
        var tbody1 = document.getElementById("myTbody1");
        var x = tbody1.childNodes.length;
        while (x-- > 0) 
        {
            tbody1.removeChild(tbody1.firstChild);
        }
        smartRow(0);
    }
}

//used
var userHitButton = false;
function handleSubmit() {
    if (userHitButton) 
    {
        return true;
    } 
    else 
    {
        return false;
    }
}

//used
function doSmartSearch() {
    userHitButton = true;
    document.smartq.submit();
}

//used
function enableStartOver() {
    $("#startOver").removeAttr("disabled");
    $("#doSearch").removeAttr("disabled");
}
