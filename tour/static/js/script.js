function SortBy(par) {
    document.querySelector('[value="'+par+'"]').setAttribute('selected', '');
    document.getElementById('id-filter-form').submit();
}