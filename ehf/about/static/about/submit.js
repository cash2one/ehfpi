/**
 * Created by jacky on 14-4-29.
 */
// change table sort arrow
$(document).ready(function () {
      //display file name
    $('#id_file').change(function () {
        var file_name = $("#id_file").val();

        $("#files").text(file_name);
        if (this.files && this.files.length) { //If this condition passes, you can get file size
            var file = this.files[0],
                fileSize = file.size || file.fileSize || 0;

            if (fileSize > 1024 * 1024 * 10) {  //5M max
                $("#files").text('');   //remove hint text
                $("#id_file").val('');  //cancel binding!!
                //popover hint
                $('#fileinput').popover({content: 'File too large(' + (fileSize / (1024 * 1024)).toFixed(1) + 'MB), maximum 10MB allowed!'});
                $('#fileinput').popover('show');
                setTimeout(function () {
                    $('#fileinput').popover('destroy');
                }, 3000);
            }
            else {
                $("#files").text(file_name + "(" + (fileSize / 1024).toFixed(1) + "KB)");
            }
        }
    });

});


