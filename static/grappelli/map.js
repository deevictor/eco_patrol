const $ = django.jQuery;
$(document).ready(function() {
    $('input#id_point').after('<div id="YMapsID" class="map YMaps YMaps-cursor-grab vTextField" style="height: 300px"></div>');
});

ymaps.ready(function () {
    var coords = $.map( $('input#id_point').val().split(','), Number );

    myMap = new ymaps.Map("YMapsID", {
        center: coords,
        zoom: 10,
        type: 'yandex#map',
        controls: ["zoomControl", "typeSelector"]
    }, {
        balloonMaxWidth: 200,
        searchControlProvider: 'yandex#search',
    });

    var myPlacemark = new ymaps.Placemark(
        coords,
        {hintContent: 'Установите метку на карте на свой объект'},
        {
            draggable: true,
            preset: 'islands#redDotIcon'
        }
    );

    myMap.geoObjects.add(myPlacemark);
});
