/**
 * Created by jacky on 14-3-18.
 */
function changeState(item){
    $("input[name='checkboxDownload']").prop("checked",$(item).prop("checked"));
}