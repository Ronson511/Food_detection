"use strict";
var ctime_tag
var submit_tag

function updateTime() {
    var now = new Date();
    ctime_tag.innerHTML = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
    setTimeout(updateTime, 1000);
}

function doSubmit() {
    $.ajax({
        url: "/qustForm/",
        data: JSON.stringify($("#myForm").formToJson()),
        contentType: 'application/json;charset=UTF-8',
        cache: false,
        // processData: false,
        // contentType: false,
        type: 'POST',
        success: function (data) {
            alert("Success! id:"+data.id);
        },
        error: function(err) {
            var resp = err.responseJSON
            if ("detail" in resp && Array.isArray(resp.detail)) {
                var msg = "null value at:"+resp.detail.map(x => x.loc[1]).join(", ")
            } else
                var msg = resp.detail
            alert('Error! '+msg);
        }
    });
}

function myInit() {
    submit_tag = document.getElementById('myXmit')
    ctime_tag  = document.getElementById('current_time')
    setTimeout(updateTime, 1000);
    submit_tag.addEventListener('click', doSubmit)
}

document.addEventListener('DOMContentLoaded', myInit, false);
