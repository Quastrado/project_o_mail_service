class CarouselSlide {
    constructor({root}) {
      // Select HTML nodes
    this.root = $(root)
    this.picture = this.root.find('.carousel-item img')
    var self = this;
    this.root.find('.carousel-control-next-icon').click(function() {self.change()})
    this.root.find('.carousel-control-prev-icon').click(function() {self.change()})
    console.log(this.root.length)
    console.log(this.picture.length)
    console.log(this.root.find('.carousel-control-next-icon').length)
    };

    change() {
        console.log('#next')
        var self = this;
        console.log(this)
        $.ajax({
            type: 'GET',
            url: '/slider',
            success: function(response) {
                self.picture.attr("src",  response)
                }
        });
    }    
};


$(document).ready(function () {
    $(".carousel.slide:not(#carouselExampleControls)").each(function( index ) {
        const slider = new CarouselSlide({root: this})
        console.log( index + ": " + $( this ).text() );
      });
});
