ymaps.ready(init);
var myMap;
var objectManager;
PAGE_WIDTH = 768;

//взял  ширину страницы 768 px как за границу между .col-md (medium devices) и col-sm (small devices)

function init() {
    // При возникновении событий, изменяющих состояние карты,
    // ее параметры передаются в адресную строку браузера (после символа #).
    // При загрузке страницы карта устанавливается в состояние,
    // соответствующее переданным параметрам.
    // http://.../savemap.html#type=hybrid&center=93.3218,60.0428&zoom=12
    myMap = new ymaps.Map("YMapsID", {
        center: [48.475544, 135.068398],
        zoom: 12,
        behaviors: ['default', 'scrollZoom'],
        controls: ['default']
    }, {
        balloonMaxWidth: 200,
        searchControlProvider: 'yandex#search',
        floatIndex: 10
        // balloonPanelMaxMapArea: 'Infinity',
    });
    myMap.controls.remove('trafficControl');
    myMap.controls.remove('geolocationControl');
    myMap.controls.remove('searchControl');
    myMap.controls.remove('fullscreenControl');

    var myButton =
        new ymaps.control.Button({
            data: {
                'content': '<b>Нажмите на карту, чтобы добавить метку</b>'
            },
            options: {
                // Зададим опции для кнопки.
                selectOnClick: false,
                maxWidth: 300
            }
        });
    myMap.controls.add(myButton, {
        float: "left",
    });

    objectManager = new ymaps.ObjectManager({
        // Чтобы метки начали кластеризоваться, выставляем опцию.
        clusterize: true,
        // ObjectManager принимает те же опции, что и кластеризатор.
        gridSize: 32,
        clusterDisableClickZoom: false,

    });

    // myPlacemarkCollection = new ymaps.GeoObjectCollection(),
    lastOpenedBalloon = false;

    var BalloonLayout = ymaps.templateLayoutFactory.createClass(
        '<div class="balloon">' +
        '<a href="#" class="label-wrapper-close"><i class="icon_close"></i></a>' +
        '$[[options.contentLayout]]' +
        '</div>',
        {
            build: function () {
                this.constructor.superclass.build.call(this);
                this._$element = $('.balloon', this.getParentElement());
                setTimeout(() => {
                    this._$element.css({right: '10px'})
                }, 100);
                this._$element.find('.label-wrapper-close')
                    .on('click', $.proxy(this.onCloseClick, this));
            },
            onCloseClick: function (e) {
                e.preventDefault();
                this.events.fire('userclose');
            },
            clear: function () {
                this._$element.css({right: '-350px'});
                this._$element.find('.close').off('click');
                this.constructor.superclass.clear.call(this);
            },
        }
    );

    var BalloonContentLayout = ymaps.templateLayoutFactory.createClass(
        '$[properties.balloonContentBody]',
        {
            build: function () {
                this.constructor.superclass.build.call(this);
                var parent = this.getParentElement();
                var share = $('.share-link', parent);
                share.popover().click(function () {
                    $('.copy-url', parent).val(window.location.href).select();
                    document.execCommand("copy");
                }).on('shown.bs.popover', function () {
                    $('.copy-url', parent).on('blur', function () {
                        share.popover('hide');
                    });
                });
                var commentsWrapper = $(".comments-wrapper", parent);
                var form = commentsWrapper.find("form");
                var addButton = commentsWrapper.find("button.add-button");
                var cancelButton = commentsWrapper.find("button[type='reset']");
                form.hide();
                addButton.click(function () {
                    form.show();
                    addButton.hide();
                });
                cancelButton.click(function () {
                    form.hide();
                    addButton.show();
                });
            },
        }
    );

    $.extend($.fancybox.defaults, {
        hash: false,
        loop: true,
    });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set({
        'preset': 'islands#darkgreenDotIcon',
        balloonPanelMaxMapArea: 0,
        balloonLayout: BalloonLayout,
        balloonContentLayout: BalloonContentLayout,
    });
    objectManager.clusters.options.set('clusterDisableClickZoom', false);
    objectManager.clusters.options.set('preset', 'islands#invertedDarkgreenClusterIcons');
    myMap.geoObjects.add(objectManager);

    $.ajax({
        url: "/label/labels_json/"
    }).done(function (data) {
        objectManager.add(data);

        // Обработка событий карты:
        // - boundschange - изменение границ области показа;
        // - type - изменение типа карты;
        // - balloonclose - закрытие балуна.
        myMap.events.add(['boundschange', 'typechange', 'balloonclose'], setLocationHash);

        // Обработка событий открытия балуна для любого элемента
        // коллекции.
        // В данном случае на карте находятся только метки одной коллекции.
        // Чтобы обработать события любых геообъектов карты можно использовать
        // myMap.geoObjects.events.add(['balloonopen'],function (e) { ...
        // Подгрузка данных после открытия балуна на объекте.
        objectManager.objects.events.add(['balloonopen'], function (e) {
            lastOpenedBalloon = e.get('objectId');
            // lastOpenedBalloon = e.get('target').properties.get('id');
            setLocationHash();
            objectManager.objects.balloon.setOptions({
                pane: 'controls',
            })
        });

        setMapStateByHash();

        // Получение значение параметра name из адресной строки браузера.
        function getParam(name, location) {
            location = location || window.location.hash;
            var res = location.match(new RegExp('[#&]' + name + '=([^&]*)', 'i'));
            return (res && res[1] ? res[1] : false);
        }

        // Передача параметров, описывающих состояние карты, в адресную строку браузера.
        function setLocationHash() {
            var params = [
                'type=' + myMap.getType().split('#')[1],
                'center=' + myMap.getCenter(),
                'zoom=' + myMap.getZoom()
            ];
            if (myMap.balloon.isOpen()) {
                params.push('open=' + lastOpenedBalloon);
            }
            window.location.hash = params.join('&');
        }

        // Установка состояния карты в соответствии с переданными в адресной строке браузера параметрами.
        function setMapStateByHash() {
            var hashType = getParam('type'),
                hashCenter = getParam('center'),
                hashZoom = getParam('zoom'),
                open = getParam('open');
            if (balloon_id) {
                objectManager.objects.balloon.open(balloon_id, {
                    balloonPanelMaxMapArea: 'Infinity'
                });

            }

            if (hashType) {
                myMap.setType('yandex#' + hashType);
            }
            if (hashCenter) {
                myMap.setCenter(hashCenter.split(','));
            }
            if (hashZoom) {
                myMap.setZoom(hashZoom);
            }
            if (open) {
                objectManager.objects.each(function (geoObj) {
                    var id = geoObj.id; //geoObj.properties.get('id'); // e.get

                    if (id == open) {
                        objectManager.objects.balloon.open(id, {
                            balloonPanelMaxMapArea: 'Infinity',
                        });
                        // geoObj.balloon.open();
                    }
                });
            }
        }
    });

    // Коллекция меток
    var myCollection = new ymaps.GeoObjectCollection();

    // // добавляем коллекцию на карту
    // myMap.geoObjects.add(myCollection);


    var pm;
    BalloonContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div id="balloonPopover">' +
        // '<a class="close" href="#">&times;</a>' +
        '<div class="arrow"></div>' +
        '<div class="popover-inner">' +
        '<h5 class="popover-title" style="width: 200px">Добавить метку на карту?</h5>' +
        '<p><button class="btn btn-primary" id="label-wrapper-show">Да</button><button class="btn btn-danger" id="label-wrapper-hide">Нет</button></p>' +
        '</div></div>', {
            build: function () {
                BalloonContentLayout.superclass.build.call(this);
                $('#label-wrapper-show').bind('click', this.onLabelClick);
                $('#label-wrapper-hide').bind('click', this.onLabelClickClose);
            },
            clear: function () {
                $('#label-wrapper-show').unbind('click', this.onLabelClick);
                $('#label-wrapper-hide').unbind('click', this.onLabelClickClose);
                BalloonContentLayout.superclass.clear.call(this);
            },
            onLabelClick: function () {
                if ($(document).width() > PAGE_WIDTH) {
                    $(".label-wrapper").css("width", "70%");
                } else {
                    $(".label-wrapper").css("width", "80%");
                }

                var myPlacemark = new ymaps.Placemark(myMap.balloon.getPosition(), {
                    name: 'new',
                });
                // добавляем в коллекцию метку
                myCollection.add(myPlacemark);
                myMap.geoObjects.add(myCollection);

                myMap.balloon.close();
            },
            onLabelClickClose: function () {
                myMap.balloon.close();
                $(".label-wrapper").css("width", "0");
            }
        });

    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        if (!myMap.balloon.isOpen()) {
            myCollection.removeAll();
            $("#id_point").val(coords);
            $(".label-wrapper").css("width", "0");
            myMap.balloon.open(coords, {
                name: "single balloon"
            }, {
                layout: BalloonContentLayout
            });
        } else {
            myMap.balloon.close();
            // myPlacemark.remove();
            // myCollection.remove();
            myCollection.removeAll();
            myMap.balloon.close();
            $(".label-wrapper").css("width", "0");
        }
    });

    $('#addMarker').bind('click', addMarkers);

    function addMarkers() {
        // Количество меток, которое нужно добавить на карту.
        var bounds = myMap.getBounds(),
            newPlacemarks = createGeoObjects(bounds);
    }




    var listBoxItems = category
            .map(function (title) {
                return new ymaps.control.ListBoxItem({
                    data: {
                        content: title
                    },
                    state: {
                        selected: true
                    },
                })
            }),
        // Теперь создадим список, содержащий 5 пунктов.
        listBoxControl = new ymaps.control.ListBox({
            data: {
                content: 'Тип метки',
                title: 'Тип метки'
            },
            items: listBoxItems,
            state: {
                // Признак, развернут ли список.
                expanded: false,
                filters: listBoxItems.reduce(function (filters, filter) {
                    filters[filter.data.get('content')] = filter.isSelected();
                    return filters;
                }, {})
            }
        });
    myMap.controls.add(listBoxControl);

    // Добавим отслеживание изменения признака, выбран ли пункт списка.
    listBoxControl.events.add(['select', 'deselect'], function (e) {
        var listBoxItem = e.get('target');
        var filters = ymaps.util.extend({}, listBoxControl.state.get('filters'));
        filters[listBoxItem.data.get('content')] = listBoxItem.isSelected();
        listBoxControl.state.set('filters', filters);
    });

    var filterMonitor = new ymaps.Monitor(listBoxControl.state);
    filterMonitor.add('filters', function (filters) {
        // Применим фильтр.
        objectManager.setFilter(getFilterFunction(filters));
    });

    function getFilterFunction(categories) {
        return function (obj) {
            var content = obj.properties.category;
            return categories[content]
        }
    }

    var searchControl = new ymaps.control.SearchControl({
        options: {
            float: 'right',
            floatIndex: 0,
            noPlacemark: true
        }
    });
    myMap.controls.add(searchControl);

}
