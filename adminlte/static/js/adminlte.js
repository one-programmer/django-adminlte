$(document).ready(function () {
    $(".click_sorting").on('click', function () {
        var desc = $(this).data('desc');
        var field = $(this).data('field');
        // 此处如果desc为0则是正序排列，点击后改为逆序排列
        var search = '?order_by=' + (desc ? "" : "-") + field;

        var form_data_array = $("#listForm").serializeArray();
        for (var i = 0; i < form_data_array.length; i++) {
            var item = form_data_array[i];
            if (item.name != 'order_by') {
                search += '&' + item.name + '=' + item.value;
            }
        }


        window.location = window.location.pathname + search;
    });

    $(".confirm-to-href-btn").on('click', function () {
        var href = $(this).data('href');
        var title = $(this).data('title') || "Are you sure?";
        console.log('start to confirm. href:', href);
        swal({
                title: title,
                type: "warning",
                showCancelButton: true,
                confirmButtonClass: "btn-danger",
                confirmButtonText: "Yes",
                closeOnConfirm: false
            },
            function () {
                console.log('confirmed!');
                window.location = href;
        });
        console.log('end to confirm');
        return false;
    });
});
