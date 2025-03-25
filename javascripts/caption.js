
(function() {
$("glightbox img").each(function() {
    var imageCaption = $(this).attr("alt");
    if (imageCaption != '') {
        $("<span class='caption'>" + imageCaption +
            "</span>").insertAfter(this);
    }
});
}