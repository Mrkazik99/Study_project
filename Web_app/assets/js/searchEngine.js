$(function () {
    $('nav').load('assets/nav.html')
})

function find(query) {
    pick_status(document.getElementById('status'));
    $('.data_row').each(function () {
        if ($(this).html().indexOf(query.value) === -1 && !$(this).hasClass("hidden")) {
            $(this).addClass('hidden');
        }
    });
}

function pick_status(select) {
    $('.data_row').each(function () {
        if (select.value === '0') {
            $(this).removeClass('hidden');
        } else if ($(this).attr('data-status') === select.value) {
            $(this).removeClass('hidden');
        } else {
            $(this).addClass('hidden');
        }
    });
    show_gone(document.getElementById('request_gone'));
}

function show_gone(check) {
    let status_select = document.getElementById('status');
    $('.data_row').each(function () {
        if (check.checked && status_select.value === '0') {
            $(this).removeClass('hidden');
        } else if (check.checked && status_select.value === $(this).attr('data-status')) {
            $(this).removeClass('hidden');
        } else if ($(this).attr('data-status').indexOf(default_hidden) !== -1) {
            $(this).addClass('hidden');
        }
    });
}