//update the result number
var resultNumber = '{{resultNumber}}';
$('#resultNumber').text(resultNumber);
$('#publicationNum').text('{{publicationNum}}');
$('#ehfNum').text('{{ehfNum}}');

//update the badge
var badge_ori = '{{badge_update}}';
var badge = badge_ori.replace(/&quot;/g, '\"');  // replace html &quot; with "
var badge_update = eval("(" + badge + ")");
$(".badge").text("");
for (var key in badge_update) {
    var keys = "#"+key;
    $(keys).text(badge_update[key]);
};
$('#pathogen_Badge').text(badge_update['all']);
$('#year_Badge').text(badge_update['all']);
$('#journal_Badge').text(badge_update['all']);
$('#phenotype_Badge').text(badge_update['all']);
$('#selectNumber').text(0);
$('#selectAllPage').prop("checked",false);