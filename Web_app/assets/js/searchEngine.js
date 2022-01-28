$(function(){$('nav').load('assets/nav.html')})
$(function(){
    $('.datepicker').datepicker({
        dateFormat: "dd-mm-yy",
        showAnim: "slideDown",
        showOtherMonths: true,
        selectOtherMonths: true,
        changeMonth: true,
        changeYear: true
    });
})