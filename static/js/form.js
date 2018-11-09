// http://ajax.microsoft.com/ajax/jquery.validate/1.7/additional-methods.js
$.validator.addMethod("lettersonly", function (value, element) {
    return this.optional(element) || /^[a-zA-Zа-яА-Я\s]+$/i.test(value);
}, "Имя не может содержать цифры");
$.validator.addMethod("noletters", function (value, element) {
    return this.optional(element) || /^[0-9-.,+\s()]+$/i.test(value);
}, "Должно содержать только цифры, проблел и символы -.,()");
$("form").validate({
    onkeyup: function (element) {
        this.element(element);
    },
    onfocusout: function (element) {
        this.element(element);
    },
    rules: {
        name: {
            required: true,
            minlength: 2,
            lettersonly: true
        },
        phone: {
            required: true,
            noletters: true
        },
        email: {
            email: true
        }
    },
    messages: {
        name: {
            required: 'Обязательно поле',
            minlength: 'Не может быть имени из одной буквы'
        },
        phone: {
            required: 'Обязательное поле',
        },
        email: {
            required: 'Обязательное поле',
            email: 'Email должен иметь формат name@domain.com'
        },
        description: {
            required: 'Обязательное поле'
        },
    }
});

$('input[name=phone]').on('keypress', function (e) {
    return String.fromCharCode(e.which).match(/[0-9\.\(\)\[\]\-\+\s\/]/) !== null;
});

$('input[name=name]').on('keypress', function (e) {
    return String.fromCharCode(e.which).match(/[a-zA-ZА-Яа-я\s\.\-\/]/) !== null;
});
