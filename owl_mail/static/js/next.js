function next() {
    $.ajax({
        type: 'GET',
        url: '/slider',
        success: function (response) {
            this.picture.attr("src", response);
        }
    });
}
