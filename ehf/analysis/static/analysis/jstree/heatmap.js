/**
 * Created by jacky on 14-3-24.
 */
URL_PREFIX = '/ehfpi';
$(function () {

    $("#jstree_div").bind("loaded.jstree", function (event, data) {
        /**
         * Open nodes on load (until x'th level)
         */
        data.instance.open_all();
//        var depth = 2;
//        data.instance.get_container().find('li').each(function (i) {
//            if (data.instance.get_path($(this)).length <= depth) {
//                data.instance.open_node($(this));
//            }
//        });
    });

    $('#jstree_div').jstree({
        "types": {
            "default": {
                "draggable": false
            },
            "kingdom": {
                "valid_children": [ "group" ]
            },
            "group": {
                "valid_children": [ "family", "genus"],
                "icon": "glyphicon glyphicon-flash"
            },
            "family": {
                "valid_children": [ "species" ]
            },
            "genus": {
                "valid_children": [ "species" ]
            },
            "species": {
                'valid_children': [ 'none' ],
                "icon": "glyphicon glyphicon-leaf"
            }
        },

        "search": {
            "fuzzy": false,
            "close_opened_onclear": true
        },

        "plugins": [ "search" , "wholerow", "checkbox", "types", "sort", "themes"]
    });

    var to = false;
    $('#plugins4_q').keyup(function () {
        if (to) {
            clearTimeout(to);
        }
        to = setTimeout(function () {
            var v = $('#plugins4_q').val();
            $('#jstree_div').jstree(true).search(v);
        }, 250);
    });

    $('#resizable').resizable({
        maxHeight: 600,
        maxWidth: 500,
        minHeight: 300,
        minWidth: 200
    });

    $('#heatMapMain').resizable({
        maxHeight: 900,
        maxWidth: 900,
        minHeight: 600,
        minWidth: 600
    });
    var a = 1;
    $('#hintWrapper').draggable({
        revert: 'valid',
        cursor: "move",
        cursorAt: { top: 56, left: 56 },
        start: function (event, ui) {
            $(this).css("z-index", a++)
        },
        cancel: ".hint"
    });

    $('#hintWrapper div').click(function () {
        $(this).addClass('top').removeClass('bottom');
        $(this).siblings().removeClass('top').addClass('bottom');
        $(this).css("z-index", a++);
    });

    $('input[name=searchNet]').clearSearch();

});

//this function validate whether the param is valid
var isValid = function valid(level, pathogen) {
    //one: whether level is in pathogen
    if (pathogen.length) {
        //parse pathogen level and pathogen group
        var pathogenLevel = new Array();
        var groupArray = new Array();

        for (var i in pathogen) {
            var levelTemp = pathogen[i].substring(0, pathogen[i].indexOf('_'));
            if (levelTemp.length) {  //maybe all
                if ($.inArray(levelTemp, pathogenLevel) == -1) {  //not in
                    pathogenLevel.push(levelTemp);
                }

                if (levelTemp == 'group') {
                    var groupTemp = pathogen[i].substring(pathogen[i].indexOf('_') + 1, pathogen[i].length - 1);
                    if ($.inArray(groupTemp, groupArray) == -1) {  //not in
                        groupArray.push(groupTemp);
                    }
                }
            }
        }

        if ($.inArray(level, pathogenLevel) != -1) {
            if (level == 'group') {
                if (groupArray.length > 1) {
                    //popover hint
                    $('#generate').popover({content: 'You can only select in one kingdom(bacteria or virus) for group level'});
                    $('#generate').popover('show');
                    setTimeout(function () {
                        $('#generate').popover('destroy');
                    }, 3000);
                    return 0;
                }
            }
            return 1;  //valid

        } else {
            //popover hint
            $('#generate').popover({content: 'Please at least select a ' + level});
            $('#generate').popover('show');
            setTimeout(function () {
                $('#generate').popover('destroy');
            }, 3000);
        }


    } else {
        //popover hint
        $('#generate').popover({content: 'please choose pathogen'});
        $('#generate').popover('show');
        setTimeout(function () {
            $('#generate').popover('destroy');
        }, 3000);

    }
    return 0;

}

var loadingTimeout = null;
// ajax request to get heatmap
function getHeatMap() {
    // get select value
    var level = $("#level").val();
    var pathogen = $("#jstree_div").jstree('get_selected');
    $("#fig").text('');

    if (isValid(level, pathogen)) {
        loadingTimeout = setTimeout('initProgressBar()', 20);
        $.post(URL_PREFIX+"/analysis/overlap/displayHeatMap", {'level': level, 'pathogen': pathogen}, evalCallbk);  //get search types from server
    }
}

function initProgressBar() {
//    $('#heatMapMain').prepend('<div id="progressbar"></div>');
//    $("#progressbar").progressbar({
//        value: false
//    });
    $('#heatMapMain').empty();
    $('#heatMapMain').append('<div id="fig" class="fig"></div>');
    //$('#heatMapMain').prepend('<div id="progressbar"><img src="/static/analysis/images/loading6.gif"/></div>');
    $('#heatMapMain').prepend('<div id="progressbar"><img src="/static/analysis/images/loading6.gif"/></div>');
}

var inited = 0;
// from http://code.google.com/p/testprogramming/source/browse/trunk/javascript/svg/d3/test/miserables.html?r=393
function evalCallbk(data) {
    inited = 1;
    clearTimeout(loadingTimeout);
    loadingTimeout = null;

    $('#heatMapMain').empty();
    $('#heatMapMain').append('<div id="fig" class="fig"></div>');

    //$("#progressbar").progressbar("destroy");
    $('#progressbar').remove();

    eval(data);

    //d3.json(miser, function (miserables) { no need for ajax call
    var matrix = [],
        nodes = miserables.nodes,
        n = nodes.length,
        type = miserables.type;

    // Compute index per node.
    nodes.forEach(function (node, i) {
        node.index = i;
        node.count = 0;
        matrix[i] = d3.range(n).map(function (j) {
            return {x: j, y: i, z: 0};
        });
    });

    // Convert links to matrix; count character occurrences.
    var maxz = 0;
    miserables.links.forEach(function (link) {
        if (link.value > maxz)
            maxz = link.value;
        if (link.source != link.target) {
            matrix[link.source][link.target].z += link.value;
            matrix[link.target][link.source].z += link.value;
            nodes[link.source].count += link.value;
            nodes[link.target].count += link.value;
        } else {
            matrix[link.source][link.target].z += link.value;
            nodes[link.source].count += link.value;
        }

    });

    var sizeMax = 60;  //maximum size of cell
    var margin = {top: 120, right: 0, bottom: 10, left: 120},
        width = (sizeMax * n > 720) ? 720 : sizeMax * n,
        height = (sizeMax * n > 720) ? 720 : sizeMax * n;

    var x = d3.scale.ordinal().rangeBands([0, width]),
        z = d3.scale.linear().domain([0, 4]).clamp(true),//cell fill-opacity, if exceed, clamp to 0-4
        c = d3.scale.category10().domain(d3.range(10));   //group color, here is ten color series.

    var svg = d3.select("#fig").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("margin-left", 0 + "px")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Precompute the orders.
    var orders = {
        name: d3.range(n).sort(function (a, b) {
            return d3.ascending(nodes[a].name, nodes[b].name);
        }),
        count: d3.range(n).sort(function (a, b) {
            return nodes[b].count - nodes[a].count;
        }),
        group: d3.range(n).sort(function (a, b) {
            return nodes[b].group - nodes[a].group;
        })
    };

// The default sort order.
    x.domain(orders.name);

    svg.append("rect")
        .attr("class", "background")
        .attr("width", width)
        .attr("height", height);

    var row = svg.selectAll(".row")
        .data(matrix)
        .enter().append("g")
        .attr("class", "row")
        .attr("transform", function (d, i) {
            return "translate(0," + x(i) + ")";
        })
        .each(row);

    row.append("line")
        .attr("x2", width);

    row.append("text")
        .attr("class", "axisText")
        .attr("x", -6)
        .attr("y", x.rangeBand() / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "end")
        .text(function (d, i) {
            return nodes[i].name;
        });

    var column = svg.selectAll(".column")
        .data(matrix)
        .enter().append("g")
        .attr("class", "column")
        .attr("transform", function (d, i) {
            return "translate(" + x(i) + ")rotate(-90)";
        });

    column.append("line")
        .attr("x1", -width);

    column.append("text")
        .attr("class", "axisText")
        .attr("x", 6)
        .attr("y", x.rangeBand() / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "start")
        .text(function (d, i) {
            return nodes[i].name;
        });

    function row(row) {
        var cell = d3.select(this).selectAll(".cell")
            .data(row.filter(function (d) {
                return d.z;
            }));
        // insert rect in the row with d.z > 0
        cell.enter().append("rect")
            .attr("class", "cell")
            .attr("x", function (d) {
                return x(d.x);
            })
            .attr("width", x.rangeBand())
            .attr("height", x.rangeBand())
            .style("fill-opacity", function (d) {
                //return z(d.z);
                return 0.3 + 7 * d.z / (10 * maxz);
            })
            .style("fill", function (d) {
                return nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : null;
            })
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("click", click)
            .append("svg:title")
            .text(function (d) {
                return '[' + nodes[d.y].name + " vs. " + nodes[d.x].name + " : " + d.z + ']';
            });

        cell.enter().append("text")
            .attr("class", "cellText")
            .attr('font-size', '12')
            .attr('fill', 'white')
            .attr('x', function (d) {
                return x(d.x) + x.rangeBand() / 2;
            })
            .attr("dx", "-1em")
            .attr("y", x.rangeBand() / 2)
            .attr("dy", ".32em")
            .on("mouseover", mouseoverText)
            .on("mouseout", mouseoutText)
            .text(function (d) {
                return d.z;
            });


    }

    function mouseoverText(p) {
        d3.selectAll(".row .axisText").classed("active", function (d, i) {
            return i == p.y;
        });
        d3.selectAll(".column .axisText").classed("active", function (d, i) {
            return i == p.x;
        });

        d3.select(this).transition().duration(100)
            .style({'font-size': 24});

    }

    function mouseoutText() {
        d3.selectAll(".axisText").classed("active", false);

        d3.select(this).transition().duration(100)
            .style({'font-size': 12});
    }

    function mouseover(p) {
        d3.selectAll(".row .axisText").classed("active", function (d, i) {
            return i == p.y;
        });
        d3.selectAll(".column .axisText").classed("active", function (d, i) {
            return i == p.x;
        });

        d3.select(this).transition().duration(100)
            .style({'stroke-opacity': 1, 'stroke': 'blue', 'stroke-width': 3});

        var item1 = nodes[p.y].name;
        var item2 = nodes[p.x].name;
        var genes;
        miserables.links.forEach(function (link) {
            if (((link.source == p.x) && (link.target == p.y)) | ((link.source == p.y) && (link.target == p.x)))
                genes = link.commonGene;
        });
        //alert(genes);
        // display common gene of current two elements
        //alert(genes.split(";").join("<br />"));
        document.getElementById("hint").innerHTML = "<b>" + item1 + "</b> vs. <b>" + item2 + "</b><br />" +
            "common genes(" + p.z + "):<br />" + genes.split(";").join("<br />");

    }

    function mouseout() {
        d3.selectAll(".axisText").classed("active", false);

        d3.select(this).transition().duration(100)
            .style({'stroke-opacity': 0});
    }

    function click(p) {
        window.open(URL_PREFIX+"/analysis/overlap/heatMapResult?a=" + nodes[p.y].acc + "&b=" + nodes[p.x].acc + "&type=" + type, "_blank");
    }

    d3.select("#order").on("change", function () {
        clearTimeout(timeout);
        order(this.value);
    });

    function order(value) {
        x.domain(orders[value]);

        var t = svg.transition().duration(2500);

        t.selectAll(".row")
            .delay(function (d, i) {
                return x(i) * 4;
            })
            .attr("transform", function (d, i) {
                return "translate(0," + x(i) + ")";
            })
            .selectAll(".cell")
            .delay(function (d) {
                return x(d.x) * 4;
            })
            .attr("x", function (d) {
                return x(d.x);
            });

        t.selectAll(".cellText")
            .delay(function (d) {
                return x(d.x) * 4;
            })
            .attr("x", function (d) {
                return x(d.x) + x.rangeBand() / 2;
            });

        t.selectAll(".column")
            .delay(function (d, i) {
                return x(i) * 4;
            })
            .attr("transform", function (d, i) {
                return "translate(" + x(i) + ")rotate(-90)";
            });
    }

    var timeout = setTimeout(function () {
        //order("group");
        //d3.select("#order").property("selectedIndex", 2).node().focus();
    }, 5000);
//});

}

//search the heatmap
function searchNet(data) {
    if (inited) {
        //reset all cell
        d3.selectAll(".cell").transition().duration(100)
            .style({'stroke-opacity': 0});
        d3.selectAll(".row .axisText").classed("active", false);
        d3.selectAll(".column .axisText").classed("active", false);

        var found = 0;
        var html='';

        var query = $('#searchNet').val();
        miserables.links.forEach(function (link) {
            var genes = link.commonGene;
            if (genes.length) {
                genes = genes.split(";")
                for (var i = 0; i < genes.length; i++) {
                    if (genes[i].toUpperCase() == query.toUpperCase()) {
                        found = 1;
                        d3.selectAll(".cell").each(function (d, i) {
                            if (((link.source == d.x) && (link.target == d.y)) | ((link.source == d.y) && (link.target == d.x))) {
                                d3.select(this).transition().duration(100)
                                    .style({'stroke-opacity': 1, 'stroke': 'blue', 'stroke-width': 3});
                            }
                        });

                        d3.selectAll(".row .axisText").classed("active", function (d, i) {
                            return i == link.source;
                        });
                        d3.selectAll(".column .axisText").classed("active", function (d, i) {
                            return i == link.target;
                        });
                        html = html+"<b>" + miserables.nodes[link.source].name + "</b> vs. <b>" + miserables.nodes[link.target].name + "</b><br />" +
            "common genes(" + link.value + "):<br />" + genes.join("<br />")+"<hr/>";
                    }
                }
            }


        });
        if (found == 0) {
            document.getElementById("hint").innerHTML = "No results";
        }else{
             document.getElementById("hint").innerHTML = html;
        }

    } else {
        //popover hint
        $('#searchButton').popover({content: 'generate heatmap first!'});
        $('#searchButton').popover('show');
        setTimeout(function () {
            $('#searchButton').popover('destroy');
        }, 3000);
    }

}

//return to search the net
function keyDown(e) {
    if (e.keyCode == 13) {
        searchNet();
    }
}

