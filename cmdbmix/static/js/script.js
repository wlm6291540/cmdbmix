$(document).ready(function () {

    function activeNav() {
        pathname = "#" + window.location.pathname.replace('/', '');
        $('.menu-open').filter(function (index, item) {
            $(item).removeClass('menu-open');
        });
        $(pathname).addClass('active');
        $(pathname).parent().parent().parent().addClass('menu-open');
    }


    activeNav();

})