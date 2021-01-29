function SortBy(par) {
    document.querySelector('[value="'+par+'"]').setAttribute('selected', '');
    document.getElementById('id-filter-form').submit();
}

$(document).ready(function(){
    /* смена языка */
    $('.change_language').click(function(e){
        e.preventDefault();
        $('#language').val($(this).attr('lang-code'));
        $('#language-option').val($(this).attr('lang-code'));
        $('#change_language_form').submit();
    });
    /* работа с фильтром */
    $('.row-slide').hide();
    $(".row-click").click(function (e) {
        e.preventDefault();
        var my_id = $(this).attr('for');
        $('#'+my_id).parent('.row-slide').slideToggle('slow');
    });
    $(".label-click").click(function (e) {
        e.preventDefault();
        var my_for = $(this).attr('for');
        $('#'+my_for).parent('.row-slide').slideToggle('slow');
        document.querySelector('[for='+my_for+']').childNodes[1].classList.toggle('down');
        document.querySelector('[for='+my_for+']').childNodes[1].classList.toggle('up');
    });
    /* скрытие правой колонки */
    $("#toggle").click(function (e) {
        e.preventDefault();
        document.querySelector('#slide-in-2').classList.toggle('slide-in-2');
        document.querySelector('#slide-in').classList.toggle('slide-out-2');
        document.querySelector('#toggle').childNodes[1].classList.toggle('right');
        document.querySelector('#toggle').childNodes[1].classList.toggle('left');
    });
});
