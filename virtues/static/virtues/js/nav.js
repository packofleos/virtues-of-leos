$(document).ready(function(){
    $nav = $('.nav');
    $toggleCollapse = $('.toggle-collapse');
    // Click even on toggle menu
    $toggleCollapse.click(function(){
        $nav.toggleClass('collapse')
    })
})
$('a[href]').each(function() {
    if ($(this).attr('href') == window.location.pathname || $(this).attr('href') == window.location.href)
        $(this).addClass('active');
});