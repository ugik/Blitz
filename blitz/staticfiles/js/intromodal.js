$(document).ready(function() {

    window.app = {};

    app.modal = undefined;
    app.showIntro = function() {
        app.modal = $('#intro-modal').modal({
            'backdrop': 'static',
            'keyboard': false,
        });
    }

    $('.intro-modal-close').click(function() { app.modal.modal('hide') });

    if (SHOW_INTRO) {
        app.showIntro();
    }

});

