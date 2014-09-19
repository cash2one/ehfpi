var json_ori = '{{data}}';
var json = json_ori.replace(/&quot;/g,'\"');  // replace html &quot; with "
miserables = eval ("("+json+")")