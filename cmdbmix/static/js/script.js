$(document).ready(function () {

    function activeNav() {
        pathname = "#" + window.location.pathname.split('/')[1];
        $('.menu-open').filter(function (index, item) {
            $(item).removeClass('menu-open');
        });
        $(pathname).addClass('active');
        $(pathname).parent().parent().parent().addClass('menu-open');
    }


    $(document).on('click', '.select-all', function (e) {
        if ($(e.target).is(':checked')) {
            $(e.target).parent().parent().parent().find('.transfer-item').find('input').filter(function (index, item) {
                $(item).prop("checked", true)
            })
        } else {
            $(e.target).parent().parent().parent().find('.transfer-item').find('input').filter(function (index, item) {
                $(item).prop("checked", false)
            })
        }
    });


    function resetSelectAll(e) {
        if (e) {
            var unchecked = $(e).parent().parent().find('input:not(:checked)').length;
            $(e).parent().parent().parent().find('.card-header').find('input').prop('checked', unchecked == 0);
        } else {
            console.log('run')
            var left = $("#left-body")
            var right = $("#right-body")
            var left_checked = left.find('input:checked').length;
            var left_all = left.find('input').length;
            left.parent().find('.card-header').find('input').prop('checked', left_checked == left_all && left_all != 0);
            var right_checked = right.find('input:checked').length;
            var right_all = right.find('input').length;
            right.parent().find('.card-header').find('input').prop('checked', right_checked == right_all && right_all != 0);
        }

    }

    function move_to_left(ids) {
        $("#right-body").find('input:checked').filter(function (index, item) {
            if (ids.indexOf(item.id) > -1) {
                $(item).parent().remove();
                $("#left-body").append($(item).parent());
            }
        });
        resetSelectAll();
    }

    function move_to_right(ids) {
        $("#left-body").find('input:checked').filter(function (index, item) {
            if (ids.indexOf(item.id) > -1) {
                $(item).parent().remove();
                $("#right-body").append($(item).parent());
            }
        });
        resetSelectAll();
    }


    function bind_role(ids, move) {
        if (ids.length != 0) {
            $.ajax({
                url: $('#url').val(),
                method: 'POST',
                headers: {'Content-Type': 'application/json;charset=utf8'},
                dataType: "json",
                data: JSON.stringify(ids),
                success: function (data) {
                    move(ids);
                    toastr.success(data.msg)
                },
                error: function (e) {
                    console.log(e)
                }

            })
        }
    };


    $(document).on('click', '#to-left', function (e) {
        var ids = [];
        $("#right-body").find('input:checked').filter(function (index, item) {
            ids.push(item.id)
        });
        bind_role(ids, move_to_left);
    });


    $(document).on('click', '#to-right', function (e) {
        var ids = [];
        $("#left-body").find('input:checked').filter(function (index, item) {
            ids.push(item.id);
        });
        bind_role(ids, move_to_right);
    });

    $(document).on('click', '.card-body>.transfer-item>input', function (e) {
        resetSelectAll(e.target);
    });


    activeNav();
    resetSelectAll();

})