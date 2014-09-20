var text = '<div class="displayNetwork">\
    <div class="row ">\
        <div class="col-md-3">\
            <div class="geneStat">\
                    <span class="geneStatTitle">EHF-drug connections</span>\
                    <span id="networkTip2"><a href="/ehfpi/help/analysisHelp#drugAnalysis" %} target="_blank"><img\
                    src="/static/images/info_20x20.png"></a></span><br/ >\
                    {% for key,value in speciesNumberAbove %}\
                        <div class="geneStatItemAbove">\
                        <input type="checkbox" id="filterGraph" value="{{ key }}"\
                               onclick="filterGraph(this)">\
                        {{ key }}: <span class="drugNumber">{{ value }}</span>\
                        </div>\
                    {% endfor %}\
                    {% for key,value in speciesNumber %}\
                        <div class="geneStatItem">\
                        <input type="checkbox" id="filterGraph" value="{{ key }}"\
                               onclick="filterGraph(this)">\
                        {{ key }}: <span class="drugNumber">{{ value }}</span>\
                        </div>\
                    {% endfor %}\
            </div>\
            <div class="searchCenter">\
                <div class="searchNetwork">\
                    Search graph:\
                    <div class="searchInput">\
                        <input type="text" class="form-control" id="searchNet" name="searchNet"\
                               placeholder="Search a drug or pathogen" onkeydown="keyDown(event);">\
                    </div>\
                    <input type="button" value="Search" id ="searchButton" class="btn btn-primary btn-sm" onclick="searchNet(this);">\
                </div>\
            </div>\
            <div class="connections" id="connections">\
                <b>Connections</b>:\
                <div id="inner-detail" contenteditable="true"></div>\
            </div>\
        </div>\
        <div class="col-md-9">\
            <div class="center-panel">\
                <div class="download"><label id="download" onclick="download(this);">Save as image</label></div>\
                <div id="zoomWrapper">\
                    <table>\
                        <tr>\
                            <td>\
                                <button id="zoomin" type="button" onclick="zoomin(this);"><span class="glyphicon glyphicon-minus"></span></button>\
                            </td>\
                            <td>\
                                <div id="zoom"></div>\
                            </td>\
                            <td>\
                                <button id="zoomout" type="button" onclick="zoomout(this);"><span class="glyphicon glyphicon-plus"></span></button>\
                            </td>\
                        </tr>\
                    </table>\
                </div>\
                <div id="log"></div>\
                <div id="infovis"></div>\
            </div>\
            <div class="legend_div" id="legend_div">\
            </div>\
        </div>\
    </div>\
</div>';
document.getElementById("main").innerHTML = text;

// init data
var json_ori = '{{toJson}}';
var json = json_ori.replace(/&quot;/g, '\"');  // replace html &quot; with "
var evalJson = eval("(" + json + ")")
init(evalJson);

//clear search using jquery-clearsearch
$('input[name=searchNet]').clearSearch();

//qtip2
$('#networkTip2').qtip({
    content: {
        title: 'Graph Operations',
        text: '<ul><li><b>Filter</b> the graph based on pathogen species, drug number is displayed on the right.</li>\
                <li><b>Mouse over</b> a node\'s label to select a node and its connections, the common drug(s) and specific drug(s) are displayed when a species is selected.</li>\
                <li>Click on the \'x\' link to <b>delete</b> a species.</li>\
                <li>You can <b>drag</b> nodes around and <b>zoom</b> and <b>pan</b>.</li>\
                <li><b>Search</b> the graph.</li>\
                <li><b>Save</b> the graph as an image.</li>\
                <li><b>Click</b> the edge to show target gene.</li></ul>'
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

