//code from infovis example
var labelType, useGradients, nativeTextSupport, animate;
URL_PREFIX = '/ehfpi';
(function () {
    var ua = navigator.userAgent,
        iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
        typeOfCanvas = typeof HTMLCanvasElement,
        nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
        textSupport = nativeCanvasSupport
            && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
    //I'm setting this based on the fact that ExCanvas provides text support for IE
    //and that as of today iPhone/iPad current text support is lame
    labelType = (!nativeCanvasSupport || (textSupport && !iStuff)) ? 'Native' : 'HTML';
    nativeTextSupport = labelType == 'Native';
    useGradients = nativeCanvasSupport;
    animate = !(iStuff || !nativeCanvasSupport);

    $('input[name=searchNet]').clearSearch();

})();

var Log = {
    elem: false,
    write: function (text) {
        if (!this.elem)
            this.elem = document.getElementById('log');
        this.elem.innerHTML = text;
        this.elem.style.left = (396 - this.elem.offsetWidth / 2) + 'px';
    }
};

var fd;

function init(json) {


    //label placement on edges, custom edge types
    $jit.ForceDirected.Plot.EdgeTypes.implement({
        'labeled-arrow': {
            'render': function (adj, canvas) {
                //plot arrow edge
                this.edgeTypes.line.render.call(this, adj, canvas);

                //get nodes cartesian coordinates
                var pos = adj.nodeFrom.pos.getc(true);
                var posChild = adj.nodeTo.pos.getc(true);

                //check for edge label in data
                var data = adj.data;

                if (data.$labelid && data.$labeltext) {
                    //if the label doesn't exist create it and append it to the label container
                    var domlabel = document.getElementById(data.$labelid);
                    if (!domlabel) {
                        domlabel = document.createElement('span');
                        domlabel.id = data.$labelid;
                        domlabel.className = 'arrow-label';
                        domlabel.innerHTML = data.$labeltext;

                        //if defined set same color as edge
                        //if(data.$color) {
                        //  domlabel.style.color = data.$color;
                        //}

                        //append the label to the labelcontainer
                        this.labels.getLabelContainer().appendChild(domlabel);
                    }

                    //now adjust the label placement
                    var ox = canvas.translateOffsetX,
                        oy = canvas.translateOffsetY,
                        sx = canvas.scaleOffsetX,
                        sy = canvas.scaleOffsetY,
                        posx = (pos.x + posChild.x) / 2 * sx + ox,
                        posy = (pos.y + posChild.y) / 2 * sy + oy,
                        s = canvas.getSize();

                    var labelPos = {
                        x: Math.round(posx - domlabel.offsetWidth / 2 +
                            s.width / 2),
                        y: Math.round(posy - domlabel.offsetHeight / 2 +
                            s.height / 2)
                    };

                    domlabel.style.left = labelPos.x + 'px';
                    domlabel.style.top = labelPos.y + 'px';
                    domlabel.style.position = "absolute";
                }
            }
        }
    });


    // init ForceDirected
    fd = new $jit.ForceDirected({
        //id of the visualization container
        injectInto: 'infovis',
        //Enable zooming and panning
        //with scrolling and DnD
        Navigation: {
            enable: true,
            type: 'Native',
            //Enable panning events only if we're dragging the empty
            //canvas (and not a node).
            panning: 'avoid nodes',
            zooming: 10 //zoom speed. higher is more sensible
        },
        // Change node and edge styles such as
        // color and width.
        // These properties are also set per node
        // with dollar prefixed data-properties in the
        // JSON structure.
        Node: {
            overridable: true,
            dim: 5
        },
        Edge: {
            overridable: true,
            lineWidth: 0.4
            //type: 'labeled-arrow'
        },

        Label: {

            type: 'HTML', //'SVG', 'Native'
            size: 10,
            textAlign: 'center',
            color: '#000'
        },

        //Add Tips
        Tips: {
            enable: true,
            onShow: function (tip, node) {
                if (!(node == undefined)) {
                    var tipDes = node.data['des'].split('_');
                    var str = "<ul>";
                    for (var i = 0; i < tipDes.length; i++) {
                        str += "<li>" + tipDes[i] + "</li>";
                    }
                    str += "</ul>";

                    tip.innerHTML = "<div class=\"customTip\"><div class=\"tip-text\">" + str + "</div></div>";
                } else {
                    tip.innerHTML = "";
                }
            }
        },

        // Add node events
        Events: {
            enable: true,
            type: 'Native',
            //Change cursor style when hovering a node
            onMouseEnter: function () {
                fd.canvas.getElement().style.cursor = 'move';
            },
            onMouseLeave: function () {
                fd.canvas.getElement().style.cursor = '';
            },
            //Update node positions when dragged
            onDragMove: function (node, eventInfo, e) {
                var pos = eventInfo.getPos();
                node.pos.setc(pos.x, pos.y);
                fd.plot();
            },
            //Implement the same handler for touchscreens
            onTouchMove: function (node, eventInfo, e) {
                $jit.util.event.stop(e); //stop default touchmove event
                this.onDragMove(node, eventInfo, e);
            }
        },
        //Number of iterations for the FD algorithm
        iterations: 200,        //Edge length
        levelDistance: 130,
        // This method is only triggered
        // on label creation and only for DOM labels (not native canvas ones).
        onCreateLabel: function (domElement, node) {
            // Create a 'name' and 'close' buttons and add them
            // to the main node label
            var nameContainer = document.createElement('span'),
                closeButton = document.createElement('span'),
                style = nameContainer.style;
            nameContainer.className = 'name';
            nameContainer.innerHTML = node.name;
            closeButton.className = 'close';
            closeButton.innerHTML = 'x';
            domElement.appendChild(nameContainer);
            if (node.data.nodeType == "species") { //only species we add close button
                domElement.appendChild(closeButton);
            }
            style.fontSize = "0.8em";
            style.color = "#000";
            //Fade the node and its connections when
            //clicking the close button
            closeButton.onclick = function () {
                node.setData('alpha', 0, 'end');
                node.eachAdjacency(function (adj) {
                    adj.setData('alpha', 0, 'end');
                });

                //if the connected node has no edges,remove also
                node.eachAdjacency(function (adj) {
                    var connected = 0;
                    adj.nodeTo.eachAdjacency(function (adjInner) {
                        if (adjInner.getData('alpha') == 1) {  //still visible node!
                            connected = connected + 1;
                        }
                    });
                    if (connected == 1) {
                        adj.nodeFrom.setData('alpha', 0, 'end');
                    }
                });

                fd.fx.animate({
                    modes: ['node-property:alpha:dim',
                        'edge-property:alpha'],
                    duration: 500
                });
            };
            //Toggle a node selection when clicking
            //its name. This is done by animating some
            //node styles like its dimension and the color
            //and lineWidth of its adjacencies.
            nameContainer.onmouseover = function () {
                //set final styles
                fd.graph.eachNode(function (n) {
                    if (n.id != node.id) delete n.selected;
                    if (n.data.$type == 'star')
                        n.setData('dim', 8, 'end');
                    else
                        n.setData('dim', 5, 'end');
                    n.eachAdjacency(function (adj) {
                        adj.setDataset('end', {
                            lineWidth: 0.4
                        });
                    });
                });
                if (!node.selected) {
                    node.selected = true;
                    if (node.data.$type == 'star')
                        node.setData('dim', 10, 'end');
                    else
                        node.setData('dim', 8, 'end');
                    node.eachAdjacency(function (adj) {
                        adj.setDataset('end', {
                            lineWidth: 3
                        });
                    });

                    node.eachAdjacency(function (adj) {
                        if (adj.nodeTo.data.$type == 'star')
                            adj.nodeTo.setData('dim', 10, 'end');
                        else
                            adj.nodeTo.setData('dim', 8, 'end');
                    });

                } else {
                    delete node.selected;
                }
                //trigger animation to final styles
                fd.fx.animate({
                    modes: ['node-property:dim',
                        'edge-property:lineWidth'],
                    duration: 500
                });
                // Build the right column relations list.
                // This is done by traversing the clicked node connections.
                var html = "<div id='nodeName'>" + node.name + "</div>";

                //for species and gene node,it is different.
                if (node.data.nodeType == 'gene') {
                    var list = [];
                    node.eachAdjacency(function (adj) {
                        if (adj.getData('alpha')) list.push(adj.nodeTo.name);
                    });
                    if (list.length > 0)
                    //append connections information
                        html = html + "<b> connections (" + list.length + "):</b>" + "<ul><li>" + list.join("</li><li>") + "</li></ul>";
                    else
                        html = html + "no connections";
                } else {
                    var commonGeneList = [];
                    var specificGeneList = [];
                    node.eachAdjacency(function (adj) {
                        var connected = 0;
                        adj.nodeTo.eachAdjacency(function (adjInner) {
                            if (adjInner.nodeTo.getData('alpha') == 1) {  //still visible node!
                                connected = connected + 1;
                            }
                        });
                        if (connected > 1) {  //common gene
                            commonGeneList.push(adj.nodeFrom.name);
                        } else {
                            specificGeneList.push(adj.nodeFrom.name);
                        }
                    });
                    html = html + "<b> connections (" + (commonGeneList.length + specificGeneList.length) + "):</b>";
                    if (commonGeneList.length > 0) {
                        html = html + "<div class='commonGene'>Common Gene (" + commonGeneList.length + ")</div><ul><li>" + commonGeneList.join("</li><li>") + "</li></ul>";
                    } else {
                        html = html + "<div class='commonGene'>Common Gene (" + commonGeneList.length + ")</div>&nbsp;No common genes";
                    }

                    if (specificGeneList.length > 0) {
                        html = html + "<div class='specific'>Specific Gene (" + specificGeneList.length + ")</div><ul><li>" + specificGeneList.join("</li><li>") + "</li></ul>";
                    } else {
                        html = html + "<div class='specific'>Specific Gene (" + specificGeneList.length + ")</div>&nbsp;No specific genes";
                    }
                    html = html + "<hr/>";
                }
                $jit.id('inner-detail').innerHTML = html;
            };

            // reset status
            nameContainer.onmouseout = function () {
                fd.graph.eachNode(function (n) {
                    delete n.selected;
                    if (n.data.$type == 'star')
                        n.setData('dim', 8, 'end');
                    else
                        n.setData('dim', 5, 'end');
                    n.eachAdjacency(function (adj) {
                        adj.setDataset('end', {
                            lineWidth: 0.4
                        });
                    });
                });
                fd.fx.animate({
                    modes: ['node-property:dim',
                        'edge-property:lineWidth'],
                    duration: 500
                });
                //$jit.id('inner-detail').innerHTML = '';
            };

        },
        // Change node styles when DOM labels are placed
        // or moved.
        onPlaceLabel: function (domElement, node) {
            var style = domElement.style;
            var left = parseInt(style.left);
            var top = parseInt(style.top);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
            style.top = (top + 10) + 'px';
            style.display = '';
        }
    });
    // load JSON data.
    fd.loadJSON(json);
    // compute positions incrementally and animate.
    fd.computeIncremental({
        iter: 40,
        property: 'end',
        onStep: function (perc) {
            Log.write(perc + '% loaded...');
        },
        onComplete: function () {
            Log.write('');
            fd.animate({
                modes: ['linear'],
                transition: $jit.Trans.Elastic.easeOut,
                duration: 2500
            });
        }
    });
    // end

    //add legend to list
    var legend_div = $jit.id('legend_div');
    legend_div.innerHTML = '<div class="nodeDes">Node:&nbsp;&nbsp;<img src="/static/analysis/images/star.png" width="12" height="12" /> pathogen &nbsp; &nbsp;' +
        '<img src="/static/analysis/images/circle.png" width="12" height="12" /> common gene&nbsp; &nbsp;' +
        '<img src="/static/analysis/images/circle1.png" width="12" height="12" /> specific gene&nbsp; &nbsp;' +
        '<img src="/static/analysis/images/triangle.png" width="12" height="12" /> gene not found</div>' +
        '<div class="edgeDes">Edge: &nbsp;&nbsp;<img src="/static/analysis/images/inhibit.png" width="50" height="7" />&nbsp;inhibit' +
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="/static/analysis/images/enhance.png" width="50" height="7" />&nbsp;increase' +
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="/static/analysis/images/other.png" width="50" height="7" />&nbsp;other</div>';

}


//this function is called from overlapNetwork, we use ajax to translate the map to the front, other than translate data to the html, and get data from html
// for js
function getNetwork() {
    var text = $('#geneList').val();
    $.get(URL_PREFIX + "/analysis/overlap/displayNetwork", {'text': text}, evalCallbk);  //get search types from server
}

//zoom in button
function zoomin(data) {
    var val = fd.controller.Navigation.zooming / 1000;
    var ans = 1 - 20 * val;
    fd.canvas.scale(ans, ans);
    //update the slider
    zoomTotal -= 20 * val;
    $("#zoom").slider("value", zoomTotal);

}

var zoomTotal = 0;

//zoom in button
function zoomout(data) {
    var val = fd.controller.Navigation.zooming / 1000;
    var ans = 1 + 20 * val;
    fd.canvas.scale(ans, ans);
    //update the slider
    zoomTotal += 20 * val;
    $("#zoom").slider("value", zoomTotal);

}

var zoomed = 0;
// the call back function for getNetwork
function evalCallbk(data) {

    eval(data);

    var a = 1;
    $('#connections').draggable({
        revert: 'valid',
        cursor: "move",
        cursorAt: { top: 56, left: 56 },
        start: function (event, ui) {
            $(this).css("z-index", a++)
        },
        cancel: ".hint"
    });

//    $('#connections div').click(function () {
//        $(this).addClass('top').removeClass('bottom');
//        $(this).siblings().removeClass('top').addClass('bottom');
//        $(this).css("z-index", a++);
//    });

    $("#zoom").slider({
        max: 4,
        min: -4,
        step: 0.2,
        value: 0,
        orientation: "horizontal",
        change: function (event, ui) {
//            if(zoomed)
//                fd.canvas.getCtx().restore();
//            fd.canvas.getCtx().save();
//
//            var val = fd.controller.Navigation.zooming/1000;
//            var value = $("#zoom").slider( "value");
//            var ans
//            if(value > 0){
//                ans = 1 + 3 * val * value;
//            }else{
//                ans = 1+val * value;
//            }
//            console.log(ans);
//            fd.canvas.scale(ans, ans);
//            zoomed = ans
        }
    });
}

//search the network
function searchNet(data) {

    //reset the graph
    fd.graph.eachNode(function (n) {
        delete n.selected;
        if (n.data.$type == 'star')
            n.setData('dim', 8, 'end');
        else
            n.setData('dim', 5, 'end');
        n.eachAdjacency(function (adj) {
            adj.setDataset('end', {
                lineWidth: 0.4
            });
        });
    });
    fd.fx.animate({
        modes: ['node-property:dim',
            'edge-property:lineWidth'],
        duration: 500
    });

    var query = $('#searchNet').val();
    var found = 0;
    if (query.length) {
        //set final styles
        fd.graph.eachNode(function (n) {
            var node = n;
            var name = node.name;
            if (name.toLowerCase() == query.toLowerCase()) {  //match exactly!
                found = 1;
                if (!node.selected) {
                    node.selected = true;
                    if (node.data.$type == 'star')
                        node.setData('dim', 10, 'end');
                    else
                        node.setData('dim', 8, 'end');
                    node.eachAdjacency(function (adj) {
                        adj.setDataset('end', {
                            lineWidth: 3
                        });
                    });

                    node.eachAdjacency(function (adj) {
                        if (adj.nodeTo.data.$type == 'star')
                            adj.nodeTo.setData('dim', 10, 'end');
                        else
                            adj.nodeTo.setData('dim', 8, 'end');
                    });

                    //hint info
                    var html = "<div id='nodeName'>" + node.name + "</div>";

                    //for species and gene node,it is different.
                    if (node.data.nodeType == 'gene') {
                        var list = [];
                        node.eachAdjacency(function (adj) {
                            if (adj.getData('alpha')) list.push(adj.nodeTo.name);
                        });
                        if (list.length > 0)
                        //append connections information
                            html = html + "<b> connections (" + list.length + "):</b>" + "<ul><li>" + list.join("</li><li>") + "</li></ul>";
                        else
                            html = html + "no connections";
                    } else {
                        var commonGeneList = [];
                        var specificGeneList = [];
                        node.eachAdjacency(function (adj) {
                            var connected = 0;
                            adj.nodeTo.eachAdjacency(function (adjInner) {
                                if (adjInner.nodeTo.getData('alpha') == 1) {  //still visible node!
                                    connected = connected + 1;
                                }
                            });
                            if (connected > 1) {  //common gene
                                commonGeneList.push(adj.nodeFrom.name);
                            } else {
                                specificGeneList.push(adj.nodeFrom.name);
                            }
                        });
                        html = html + "<b> connections (" + (commonGeneList.length + specificGeneList.length) + "):</b>";
                        if (commonGeneList.length > 0) {
                            html = html + "<div class='commonGene'>Common Gene (" + commonGeneList.length + ")</div><ul><li>" + commonGeneList.join("</li><li>") + "</li></ul>";
                        } else {
                            html = html + "<div class='commonGene'>Common Gene (" + commonGeneList.length + ")</div>&nbsp;No common genes";
                        }

                        if (specificGeneList.length > 0) {
                            html = html + "<div class='specific'>Specific Gene (" + specificGeneList.length + ")</div><ul><li>" + specificGeneList.join("</li><li>") + "</li></ul>";
                        } else {
                            html = html + "<div class='specific'>Specific Gene (" + specificGeneList.length + ")</div>&nbsp;No specific genes";
                        }
                        html = html + "<hr/>";
                    }
                    $jit.id('inner-detail').innerHTML = html;

                }
            }
        });

        if (found == 0) {
            $jit.id('inner-detail').innerHTML = "no results";
        }

        //trigger animation to final styles
        fd.fx.animate({
            modes: ['node-property:dim',
                'edge-property:lineWidth'],
            duration: 500
        });


    }
}

//return to search the net
function keyDown(e) {
    if (e.keyCode == 13) {
        searchNet();
    }
}

function download(data) {
    var mycanvas = document.getElementById("infovis");
    html2canvas(mycanvas, {
        onrendered: function (canvas) {
            window.open(canvas.toDataURL("image/png"));
        }
    });
}

//download orginal csv file that generates the graph, added: 20140812
function downloadCSV(data) {
    URL_PREFIX = '/ehfpi';
    var text = $('#geneList').text();
    //var aboveSpeciesList = $('#aboveSpeciesList').text();

    var csrf = $('#csrf').attr("value");
    var index = csrf.indexOf('value=');
    var index2 = csrf.lastIndexOf("'");
    var csrfmiddlewaretoken = csrf.substr(index + 7, index2 - index - 7);

    $.fileDownload(URL_PREFIX + '/analysis/overlap/downloadCSV',
        {
            httpMethod: "POST",
            data: {
                text: text,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            }
        })
        .done(function () {
        })
        .fail(function () {
            alert('File download failed!');
        });

}

//left top, when click the checkbox, highlight the corresponding species
function filterGraph(item) {
    //reset the graph
    fd.graph.eachNode(function (n) {
        delete n.selected;
        if (n.data.$type == 'star')
            n.setData('dim', 8, 'end');
        else
            n.setData('dim', 5, 'end');
        n.eachAdjacency(function (adj) {
            adj.setDataset('end', {
                lineWidth: 0.4
            });
        });
    });
    fd.fx.animate({
        modes: ['node-property:dim',
            'edge-property:lineWidth'],
        duration: 500
    });

    //check all checkbox
    var specliesList = new Array();
    var geneList = new Array();
    var html = ""
    $("input[id ='filterGraph']").each(function () {
        if ($(this).prop("checked")) {
            specliesList.push($(this).val());
            var query = $(this).val();

            //set final styles
            fd.graph.eachNode(function (n) {
                var node = n;
                if (node.name == query) {  //match exactly!
                    if (!node.selected) {
                        node.selected = true;
                        if (node.data.$type == 'star')
                            node.setData('dim', 10, 'end');
                        else
                            node.setData('dim', 8, 'end');
                        node.eachAdjacency(function (adj) {
                            adj.setDataset('end', {
                                lineWidth: 3
                            });
                        });

                        node.eachAdjacency(function (adj) {
                            if (adj.nodeTo.data.$type == 'star')
                                adj.nodeTo.setData('dim', 10, 'end');
                            else
                                adj.nodeTo.setData('dim', 8, 'end');
                        });

                        //hint info
                        html = html + "<div id='nodeName'>" + node.name + "</div>";

                        var commonGeneList = [];
                        var specificGeneList = [];
                        node.eachAdjacency(function (adj) {
                            var connected = 0;
                            adj.nodeTo.eachAdjacency(function (adjInner) {
                                if (adjInner.nodeTo.getData('alpha') == 1) {  //still visible node!
                                    connected = connected + 1;
                                }
                            });
                            if (connected > 1) {  //common gene
                                commonGeneList.push(adj.nodeFrom.name);
                            } else {
                                specificGeneList.push(adj.nodeFrom.name);
                            }
                        });
                        html = html + "<b> connections (" + (commonGeneList.length + specificGeneList.length) + "):</b>";
                        if (commonGeneList.length > 0) {
                            html = html + "<div class='commonGene'>Common Gene (" + commonGeneList.length + ")</div><ul><li>" + commonGeneList.join("</li><li>") + "</li></ul>";
                        } else {
                            html = html + "<div class='commonGene'>Common Gene (" + commonGeneList.length + ")</div>&nbsp;No common genes";
                        }

                        if (specificGeneList.length > 0) {
                            html = html + "<div class='specific'>Specific Gene (" + specificGeneList.length + ")</div><ul><li>" + specificGeneList.join("</li><li>") + "</li></ul>";
                        } else {
                            html = html + "<div class='specific'>Specific Gene (" + specificGeneList.length + ")</div>&nbsp;No specific genes";
                        }
                        html = html + "<hr/>";


                    }
                }
            });
            $jit.id('inner-detail').innerHTML = html;


            //trigger animation to final styles
            fd.fx.animate({
                modes: ['node-property:dim',
                    'edge-property:lineWidth'],
                duration: 500
            });

        }
    });

}