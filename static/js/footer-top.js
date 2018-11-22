$(".footer-top-image").click(function (e) {
    var id = $(this).data("id");
    var obj = myMap.geoObjects.get(0).objects.balloon;
    var coordinates = obj._collection.balloon._collection._objectsById[id].geometry.coordinates;
    obj.open(id);
    myMap.setCenter(coordinates, 17, {
        checkZoomRange: true
    });
});
