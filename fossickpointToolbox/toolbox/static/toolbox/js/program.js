var csrf_token = getCookie('csrftoken');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});
$(document).ready(function(){
    var contentList = document.getElementById('contentList');
    var sortable = Sortable.create(contentList, {group: "content"});

    var programList = document.getElementById('programList');
    var sortable2 = Sortable.create(programList, {group: "content"});
    // Sortable.create(qux,{
    //     group:{
    //         name: 'qux',
    //         put: ['content','program']
    //     },
    //     animation:100
    // })
})

function updateProgram()
{
    var programList = $("#programList li");
    var form = new FormData();
    programList.each(function(index){
        form.append(index, $(this).attr("id"));
    })
    $.ajax({
        type:'POST',
        url:  location.href,
        data:form,
        processData:false,  // 告诉jquery不转换数据
        contentType:false,  // 告诉jquery不设置内容格式

        success:function (arg) {
            if (arg["status"] == "1")
            {
                alert("update program successfully");
                location.reload();

            }
            else
            {
                alert("create program failed");

            }
        }
    });
}