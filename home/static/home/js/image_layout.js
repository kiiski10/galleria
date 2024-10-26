document.addEventListener('DOMContentLoaded', function() {
    // init Masonry
    var grid = document.querySelector('.grid');
    var msnry = new Masonry(grid, {
        itemSelector: '.grid-item',
        columnWidth: 200,
        gutter: 4,
        fitWidth: true,
    });

    // layout Masonry after each image loads
    imagesLoaded(grid).on('progress', function() {
        msnry.layout();
    });

    window.addEventListener('resize', function() {
        msnry.layout();
    });
});