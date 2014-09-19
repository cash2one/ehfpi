/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {
    //qtip2
    $('#ppiNetworkTip').qtip({
        content: {
            title: 'Graph Operations',
            text: '<ul><li><b>Click</b> a node to select a node and its connections, the information of connected nodes are displayed.</li>\
                <li>You can <b>drag</b> nodes around and <b>zoom</b> and <b>pan</b>.</li>\
                <li><b>Save</b> the graph (entire or current) as an image.</li>\
                <li><b>Search</b> the graph.</li></ul>'
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
});

//callback function of the ajax call
function evalCallbk(data) {  //data is the gene list
    $('#otherLoading').remove();  //remove the image
    $('#ppiView').removeClass('hidePPI');

    eval(data);
}

//init the graph
function init(elements) {
    var layout_defaults;
    if (elements.nodes.length < 500) {
        layout_defaults = ({
            name: 'arbor',   //null,random,preset,grid,circle,concentric,breadthfirst,arbor,cose

            liveUpdate: false, // whether to show the layout as it's running
            ready: undefined, // callback on layoutready
            stop: undefined, // callback on layoutstop
            maxSimulationTime: 3000, // max length in ms to run the layout
            fit: true, // reset viewport to fit default simulationBounds
            padding: [ 50, 50, 50, 50 ], // top, right, bottom, left
            simulationBounds: undefined, // [x1, y1, x2, y2]; [0, 0, width, height] by default
            ungrabifyWhileSimulating: true, // so you can't drag nodes during layout

            // forces used by arbor (use arbor default on undefined)
            repulsion: undefined,
            stiffness: undefined,
            friction: undefined,
            gravity: true,
            fps: undefined,
            precision: undefined,

            // static numbers or functions that dynamically return what these
            // values should be for each element
            nodeMass: undefined,
            edgeLength: undefined,

            stepSize: 1, // size of timestep in simulation

            // function that returns true if the system is stable to indicate
            // that the layout can be stopped
            stableEnergy: function (energy) {
                var e = energy;
                return (e.max <= 0.5) || (e.mean <= 0.3);
            }
        });
    } else {
        layout_defaults = ({
            name: 'random',
            ready: undefined, // callback on layoutready
            stop: undefined, // callback on layoutstop
            fit: true // whether to fit to viewport
        });
    }

    console.log(layout_defaults.name);

    cy = cytoscape(options = {   //global accessible dom
        container: document.getElementById('cy'),
        layout: layout_defaults,   //layout: null, random, preset, grid, circle, concentric, breadthfirst,arbor, coSE

        zoom: 1,  //default zoom
        minZoom: 0.1,  //minimum zoom
        maxZoom: 10,   //maximum zoom
        zoomingEnabled: true,
        userZoomingEnabled: true,
        pan: {x: 0, y: 0},
        userPanningEnabled: true,
        hideEdgesOnViewport: false,
        hideLabelsOnViewport: false,
        textureOnViewport: true,
        renderer: { /* ... */ },
        style: [
            {
                selector: 'node',
                css: {
                    'content': 'data(name)',
                    'font-family': 'helvetica',
                    'font-size': 12,
                    'text-outline-width': 1,
                    'text-outline-color': '#000',
                    'text-valign': 'top',
                    'color': '#fff',
                    'width': 'mapData(weight, 0, 200, 20, 50)',
                    'height': 'mapData(height, 0, 200, 20, 50)',
                    'border-color': '#fff'
                }
            },

            {
                selector: 'node:selected',
                css: {
                    'shape': 'star',   //rectangle, roundrectangle, ellipse, triangle, pentagon, hexagon, heptagon, octagon, star
                    'width': 'mapData(weight, 0, 200, 30, 75)',
                    'height': 'mapData(height, 0, 200, 30, 75)',
                    'font-size': 20,
                    'color': '#F2572D',
                    'text-outline-width': 0

                }
            },

            {
                selector: 'node.selected',
                css: {
                    'shape': 'star',   //rectangle, roundrectangle, ellipse, triangle, pentagon, hexagon, heptagon, octagon, star
                    'width': 'mapData(weight, 0, 200, 30, 75)',
                    'height': 'mapData(height, 0, 200, 30, 75)',
                    'font-size': 20,
                    'color': '#F2572D'

                }
            },

            {
                selector: 'edge:selected',
                css: {
                    'width': 2.5,
                    'color': '#F2572D'
                }
            },

            {
                selector: 'edge.selected',
                css: {
                    'width': 2.5,
                    'color': '#F2572D'
                }
            },

            {
                selector: 'edge',
                css: {
                    'width': 1.5,
                    'curve-style': 'haystack',  //ellipse,rectangle,bezier,haystack
                    'line-color': '#88A0BF',
                    'target-arrow-shape': 'none'  //tee, triangle, square, circle, diamond, or none.
                }
            },

            {
                selector: '.submitted',
                css: {
                    'content': 'data(name)',
                    'font-family': 'helvetica',
                    'font-size': 12,
                    'text-outline-width': 1,
                    'text-outline-color': '#000',
                    'min-zoomed-font-size': 4,
                    'text-valign': 'top',
                    'background-color': '#F2572D',
                    'width': 'mapData(height, 0, 200, 20, 50)',
                    'height': 'mapData(height, 0, 200, 20, 50)',
                    'border-color': '#fff'
                }
            },

            {
                selector: '.other',
                css: {
                    'content': 'data(name)',
                    'font-family': 'helvetica',
                    'color': '#000',
                    'font-size': 12,
                    'text-outline-width': 0,
                    'text-outline-color': '#000',
                    'min-zoomed-font-size': 4,
                    'text-valign': 'top',
                    'background-color': '#005BAC',
                    'width': 'mapData(height, 0, 200, 20, 50)',
                    'height': 'mapData(height, 0, 200, 20, 50)',
                    'border-color': '#fff'
                }

            }
        ],


        ready: function () {
            //add navigator here
            //$('#cy').cytoscapeNavigator();
            //add qtip
            // just use the regular qtip api but on cy elements
            cy.elements('node').qtip({
                content: function () {
                    var outStr = '<a href="http://www.hprd.org/summary?hprd_id=' + this.data().hprd + '&isoform_id=' + this.data().hprd + '_1&isoform_name=Isoform_1" target="_blank" title="link to HPRD">HPRD: ' + this.data().hprd + '</a><br/>';

                    outStr += "<b>Related Nodes:</b> <br/>";

                    this.neighborhood("node").each(function (i, elem) {
                        outStr += elem.id() + '(<a href="http://www.ncbi.nlm.nih.gov/protein/' + elem.data().refseqId + '" target="_blank" title="link to NCBI Refseq">' + elem.data().refseqId + '</a>)<br/>';
                    });
                    return outStr;
                },
                position: {
                    my: 'top center',
                    at: 'bottom center'
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

            cy.elements('edge').qtip({
                content: function () {
                    var pubmedId = this.data().pubmedId.split(',');
                    var outStr = 'expType: ' + this.data().expType + '<br/>' + 'pubmedId: ';
                    for (var i = 0; i < pubmedId.length; i++) {
                        outStr += '<a href="http://www.ncbi.nlm.nih.gov/pubmed/?term=' + pubmedId[i] + '" target="_blank">' + pubmedId[i] + '</a> '
                    }

                    return outStr
                },
                position: {
                    my: 'top center',
                    at: 'bottom center'
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

        }
    });

    cy.load(elements, function (e) {
        console.log("cy loaded elements");
    }, function (e) {
        //add navigator
        $('#cy').cytoscapeNavigator({
            // options go here
        });
        console.log("cy laid out elements");
    });

    //add panzoom here
    // the default values of each option are outlined below:
    var panzoom_defaults = ({
        zoomFactor: 0.05, // zoom factor per zoom tick
        zoomDelay: 45, // how many ms between zoom ticks
        minZoom: 0.1, // min zoom level
        maxZoom: 10, // max zoom level
        fitPadding: 50, // padding when fitting
        panSpeed: 10, // how many ms in between pan ticks
        panDistance: 10, // max pan distance per tick
        panDragAreaSize: 75, // the length of the pan drag box in which the vector for panning is calculated (bigger = finer control of pan speed and direction)
        panMinPercentSpeed: 0.25, // the slowest speed we can pan by (as a percent of panSpeed)
        panInactiveArea: 8, // radius of inactive area in pan drag box
        panIndicatorMinOpacity: 0.5, // min opacity of pan indicator (the draggable nib); scales from this to 1.0
        autodisableForMobile: true, // disable the panzoom completely for mobile (since we don't really need it with gestures like pinch to zoom)

        // icon class names
        sliderHandleIcon: 'fa fa-minus',
        zoomInIcon: 'fa fa-plus',
        zoomOutIcon: 'fa fa-minus',
        resetIcon: 'fa fa-expand'
    });

    cy.panzoom(panzoom_defaults);

    cy.on('click', '', { foo: 'bar' }, function (evt) {  //reset all node
        cy.elements('node.selected').removeClass('selected');  //remove all selected node
    })

    cy.on('click', 'node', { foo: 'bar' }, function (evt) {
        var node = evt.cyTarget;

        node.neighborhood().each(function (i, elem) {
            elem.addClass('selected');
        })

    });


}


//save image
function saveGraph(data) {
    var scope = $('#scope').val();
    var option;
    if (scope == 'current') {
        option = {
            full: false
        };
    } else {
        option = {
            full: true
        };
    }
    var pngData = cy.png(option);
    window.open(pngData);

}

//return to search the net
function keyDown(e) {
    if (e.keyCode == 13) {
        searchNet();
    }
}

function searchNet() {
    var query = $('#searchGraph').val();
    var found = 0;
    cy.elements('node.selected').removeClass('selected');  //remove all selected node
    if (query.length) {
        cy.elements("node").each(function (i, elem) {
            if (elem.id().toUpperCase() == query.toUpperCase() | elem.data().hprd.toUpperCase() == query.toUpperCase() | elem.data().refseqId.toUpperCase() == query.toUpperCase()) {
                found = 1;
                elem.addClass('selected');
                elem.neighborhood().each(function (j, ele) {
                    ele.addClass('selected');
                })
                $('#searchGraphButton').popover({content: 'Results exist!'});
                $('#searchGraphButton').popover('show');
                setTimeout(function () {
                    $('#searchGraphButton').popover('destroy');
                }, 3000);
            }

        });
    }

    if (found == 0) {
        $('#searchGraphButton').popover({content: 'no match!'});
        $('#searchGraphButton').popover('show');
        setTimeout(function () {
            $('#searchGraphButton').popover('destroy');
        }, 3000);
    }
}