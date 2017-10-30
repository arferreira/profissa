(function ($) {
    // USE STRICT
    "use strict";
    $(window).on('load', function () {

        // PAGE LOADER
        var $page_loader = $('#page-loader');
        $page_loader.fadeOut(500);

        // TESTIMONIALS SLIDER
        var $testimonials_slider = $('.testimonials-slider');
        if ($testimonials_slider.length > 0) {
            $testimonials_slider.owlCarousel({
                navigation: false, // Show next and prev buttons
                slideSpeed: 300,
                autoPlay: 3000,
                paginationSpeed: 400,
                singleItem: true,
                pagination: true

            });
        }


        // PARTNERS SLIDER
        var $partners_slider = $('.partners-slider');
        if ($partners_slider.length > 0) {
            $partners_slider.owlCarousel({
                autoPlay: 3000, //Set AutoPlay to 3 seconds
                pagination: true,
                items: 5,
                itemsDesktop: [1199, 3],
                itemsDesktopSmall: [979, 3]

            });
        }

        // MASONRY GRID BLOG
        var $grid = $('.masonry-grid');
        if ($grid.length > 0) {
            $grid.imagesLoaded(function () {
                // init Masonry after all images have loaded
                $grid.masonry({
                    itemSelector: ".masonry-item"
                });
            });
        }

        // CONTER UP

        var $count = $('.count');
        if ($count.length > 0) {
            $count.counterUp({
                delay: 10,
                time: 1000
            });
        }

        // TYPE IT
        var $typeit = $('.landing_provider');
        if ($typeit.length > 0) {
            $typeit.typeIt({
                strings: ['A melhor plataforma para prestadores de serviço!']
            });
        }
        
        //MAGNIFIC POPUP
        var $link = $('.popup-link');
        if ($link.length > 0) {
            $link.magnificPopup({
                disableOn: 700,
                type: 'iframe',
                mainClass: 'mfp-fade',
                removalDelay: 160,
                preloader: false,
                fixedContentPos: false
            });
        }
        
        // GOOGLE MAP
        var $google_map = $('.google-map');

        if ($google_map.length > 0) {
            $google_map.each(function () {
                // getting options from html 
                var Self = $(this);
                var mapName = Self.attr('id');
                var mapLat = Self.data('map-lat');
                var mapLng = Self.data('map-lng');
                var iconPath = Self.data('icon-path');
                var mapZoom = Self.data('map-zoom');
                var mapTitle = Self.data('map-title');


                var styles = [
                    {
                        "featureType": "administrative",
                        "elementType": "labels.text.fill",
                        "stylers": [
                            {
                                "color": "#444444"
                            }
                        ]
                    },
                    {
                        "featureType": "landscape",
                        "elementType": "all",
                        "stylers": [
                            {
                                "color": "#f2f2f2"
                            }
                        ]
                    },
                    {
                        "featureType": "landscape",
                        "elementType": "geometry.fill",
                        "stylers": [
                            {
                                "color": "#e4e3e3"
                            }
                        ]
                    },
                    {
                        "featureType": "landscape.man_made",
                        "elementType": "labels.text.fill",
                        "stylers": [
                            {
                                "color": "#797979"
                            }
                        ]
                    },
                    {
                        "featureType": "poi",
                        "elementType": "all",
                        "stylers": [
                            {
                                "visibility": "off"
                            }
                        ]
                    },
                    {
                        "featureType": "road",
                        "elementType": "all",
                        "stylers": [
                            {
                                "saturation": -100
                            },
                            {
                                "lightness": 45
                            }
                        ]
                    },
                    {
                        "featureType": "road",
                        "elementType": "geometry",
                        "stylers": [
                            {
                                "color": "#d8d7d7"
                            }
                        ]
                    },
                    {
                        "featureType": "road",
                        "elementType": "labels.text.fill",
                        "stylers": [
                            {
                                "color": "#acabab"
                            }
                        ]
                    },
                    {
                        "featureType": "road.highway",
                        "elementType": "all",
                        "stylers": [
                            {
                                "visibility": "simplified"
                            }
                        ]
                    },
                    {
                        "featureType": "road.arterial",
                        "elementType": "labels.icon",
                        "stylers": [
                            {
                                "visibility": "off"
                            }
                        ]
                    },
                    {
                        "featureType": "transit",
                        "elementType": "all",
                        "stylers": [
                            {
                                "visibility": "off"
                            }
                        ]
                    },
                    {
                        "featureType": "water",
                        "elementType": "all",
                        "stylers": [
                            {
                                "color": "#e1e0e0"
                            },
                            {
                                "visibility": "on"
                            }
                        ]
                    }
                ];


                // if zoom not defined the zoom value will be 15;
                if (!mapZoom) {
                    var mapZoom = 12;
                }
                ;
                // init map
                var map;
                map = new GMaps({
                    div: '#' + mapName,
                    scrollwheel: false,
                    lat: mapLat,
                    lng: mapLng,
                    styles: styles,
                    zoom: mapZoom
                });
                // if icon path setted then show marker
                if (iconPath) {

                    map.addMarker({
                        icon: iconPath,
                        lat: 40.925372,
                        lng: -74.276544,
                        title: 'Fedrex',
                        infoWindow: {
                            content: '<h6>Head office 12 sector 7</h6> <p>Ada Rood-15 H#12 Texas, USA</p>'
                        }
                    });
                }
            });
        }

        // CONTACT FORM
        var $contact = $('#ContactForm');
        if ($contact.length > 0) {
            $contact.validator().on('submit', function (e) {
                var message = '';
                if (e.isDefaultPrevented()) {
                    alert('Your Form Contain Invalid Fields');
                } else {
                    e.preventDefault();
                    //Send Contact Mail AJAX
                    var formdata = jQuery("#ContactForm").serialize();
                    jQuery.ajax({
                        type: "POST",
                        url: "contact_form/contact.php",
                        data: formdata,
                        dataType: 'json',
                        async: false,
                        success: function (data) {
                            if (data.success) {
                                alert("Your Message has been Sent!");
                            } else {
                                alert("Error On Sending Message!");
                            }

                        },
                        error: function (error) {
                            alert("Something Went Wrong!");
                        }

                    });
                }
            });
        }

        // DEMO REQUEST FORM
        var $demo = $('#DemoRequestForm');
        if ($demo.length > 0) {
            $demo.validator().on('submit', function (e) {
                var message = '';
                if (e.isDefaultPrevented()) {
                    alert('Your Form Contain Invalid Fields');
                } else {
                    e.preventDefault();
                    //Send Demo Request Mail AJAX
                    var formdata = jQuery("#DemoRequestForm").serialize();
                    jQuery.ajax({
                        type: "POST",
                        url: "contact_form/demo-request.php",
                        data: formdata,
                        dataType: 'json',
                        async: false,
                        success: function (data) {
                            if (data.success) {
                                alert("Your Message has been Sent!");
                            } else {
                                alert("Error On Sending Message!");
                            }

                        },
                        error: function (error) {
                            alert("Something Went Wrong!");
                        }

                    });
                }
            });
        }
    });
})(jQuery);