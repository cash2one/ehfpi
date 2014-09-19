tinyMCE.init({
	// General options
	mode : "textareas",
	theme : "modern",
	//plugins : "pagebreak,layer,table,save,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,template,wordcount,advlist,autosave",
    //plugins: "advlist anchor autolink autoresize autosave bbcode lists link image charmap print preview hr pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking save table contextmenu directionality emoticons template paste textcolor",
    plugins: "advlist anchor autolink autoresize autosave charmap code contextmenu directionality emoticons fullpage fullscreen hr image insertdatetime link lists importcss media nonbreaking noneditable pagebreak paste preview print save searchreplace spellchecker tabfocus table template textcolor visualblocks visualchars wordcount",

	// Theme options
	theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,styleselect,formatselect,fontselect,fontsizeselect,fullscreen,code",
	theme_advanced_buttons2 : "cut,copy,paste,pastetext,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,|,insertdate,inserttime,preview,|,forecolor,backcolor",
	theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl",

	theme_advanced_toolbar_location : "top",
	theme_advanced_toolbar_align : "left",
	theme_advanced_statusbar_location : "bottom",
	theme_advanced_resizing : true,

	// Example content CSS (should be your site CSS)
	//content_css : "/static/tinymce/style.css",

	template_external_list_url : "lists/template_list.js",
	external_link_list_url : "lists/link_list.js",
	external_image_list_url : "lists/image_list.js",
	media_external_list_url : "lists/media_list.js",

	// Style formats
	style_formats : [
		{title : 'Bold text', inline : 'strong'},
		{title : 'Red text', inline : 'span', styles : {color : '#ff0000'}},
		{title : 'Help', inline : 'strong', classes : 'help'},
		{title : 'Table styles'},
		{title : 'Table row 1', selector : 'tr', classes : 'tablerow'}
	],

	width: '700',
	height: '400'

});