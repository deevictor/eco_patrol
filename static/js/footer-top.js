$(".footer-top-image").click(function (e) {
    var id = $(this).data("id");
    var obj = myMap.geoObjects.get(0).objects.balloon;
    obj.open(id);
    var coordinate = obj.getPosition();
    myMap.setCenter(coordinate, 17, {
    checkZoomRange: true
    });
});
