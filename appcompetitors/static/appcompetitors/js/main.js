$(function() {
    // source: https://code.luasoftware.com/tutorials/bootstrap/bootstrap4-navbar-hide-when-scroll-down/
    // add class="fixed-top" to navbar
    var lastScrollTop = 0;
    var $navbar = $('.navbar');
    var navbarHeight = $navbar.outerHeight();
    var movement = 0;
    var lastDirection = 0;

    $(window).scroll(function(event) {
        var st = $(this).scrollTop();
        movement += st - lastScrollTop;

        if (st > lastScrollTop) { // scroll down
            if (lastDirection != 1) {
                movement = 0;
            }
            var margin = Math.abs(movement);
            if (margin > navbarHeight) {
                margin = navbarHeight;
            }
            margin = -margin;
            $navbar.css('margin-top', margin + "px")

            lastDirection = 1;
        } else { // scroll up
            if (lastDirection != -1) {
                movement = 0;
            }
            var margin = Math.abs(movement);
            if (margin > navbarHeight) {
                margin = navbarHeight;
            }
            margin = margin - navbarHeight;
            $navbar.css('margin-top', margin + "px")

            lastDirection = -1;
        }

        lastScrollTop = st;
        // console.log(margin);
    });
});

// $(function() {
//     // source: https://code.luasoftware.com/tutorials/bootstrap/bootstrap4-navbar-hide-when-scroll-down/
//     var lastScrollTop = 0;
//     var $navbar = $('.navbar');
//
//     $(window).scroll(function(event) {
//         var st = $(this).scrollTop();
//
//         if (st > lastScrollTop) { // scroll down
//             use this to use CSS3 animation
//             $navbar.addClass("fade-out");
//             $navbar.removeClass("fade-in");
//
//             // use this if no effect is required
//             // $navbar.hide();
//         } else { // scroll up
//             use this to use CSS3 animation
//             $navbar.addClass("fade-in");
//             $navbar.removeClass("fade-out");
//
//             // use this if no effect is required
//             // $navbar.show();
//         }
//         lastScrollTop = st;
//     });
// });
