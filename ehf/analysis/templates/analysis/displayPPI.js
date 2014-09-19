// init data
var json_ori = '{{toJson}}';
var json = json_ori.replace(/&quot;/g, '\"');  // replace html &quot; with "
var evalJson = eval("(" + json + ")")
init(evalJson);
