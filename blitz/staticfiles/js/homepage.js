'use strict';

(function() {
    var FEEDITEM_OFFSET = 0;

    jQuery(document).ready(function($) {
        // Hack to Fix Exercice Matrix borders
        // TODO: Make it happen just with HTML and CSS, without javascript help
        function fixExerciseMatrixBorders(containerHTML) {

            var $exercises = containerHTML.find('.exercise-matrix .exercise-container');
            var i = 0;
            for (i = 0; i < $exercises.length; i++) {
                var $el = $exercises.eq(i),
                    oddLen = 0,
                    evenLen = 0;

                if ($el.hasClass('odd')) {
                    var oddLen = $el.find('.exercise-details-container .detail').length;
                    if (oddLen > 0) {
                        var oddHeight = oddLen>1? (oddLen*25):31;
                        $el.find('.exercise-name').css('height', oddHeight);
                    }

                    if ($el.next() && $el.next().hasClass('even')) {
                        var $elEven = $el.next();
                        var evenLen = $elEven.find('.exercise-details-container .detail').length;

                        if (evenLen > 0) {
                            var evenHeight = evenLen>1? (evenLen*25):31;
                            $elEven.find('.exercise-name').css('height', evenHeight);
                        }

                        if (oddLen > evenLen) {
                            $elEven.find('.exercise-name').css('height', oddHeight);
                        }

                        if (evenLen > oddLen) {
                            $el.find('.exercise-name').css('height', evenHeight);
                        }
                    };
                };
            }
            return containerHTML;
        }
        // END

        // Shows progress indicator
        function homepage_setLoading() {
            $('#homepage-loadmore').hide();
            $('#homepage-loading').show();
        }

        // Loads and render feed items
        function homepage_morefeed() {
            homepage_setLoading();
            $.get('/api/blitz_feed',
                {'offset': FEEDITEM_OFFSET},
                function(data) {
                    for (var i=0; i<data.feeditems.length; i++) {
                        var item = data.feeditems[i];
                        var $el = $(item.html);

                        if ($el.find('.exercise-matrix .exercise-container')) {
                            $el = fixExerciseMatrixBorders($el);
                        }

                        $('#main-feed').append($el);
                    }
                    FEEDITEM_OFFSET = data.offset;
                    $('#homepage-loadmore').show();
                    $('#homepage-loading').hide();
                }
            );
        }

        // add comment button show/hide
        $('#add-comment').on('focus', function() {
            $('#add-comment-submit').show(300);
        });
        $('#add-comment').on('blur', function() {
            if ($(this).val() == "" && $('#id_picture').val() == "") {
                $('#add-comment-submit').hide(300);
            }
        });
        $('#id_picture').on('change', function() { $('#add-comment-submit').show(300); });
        $('input[type=file]').change(function(e) { document.getElementById("id_label").innerHTML = "&#10004;"; });

        // add comment submit
        $('#add-comment-submit').on('click', function(e) {
            e.preventDefault();
            var comment_text = $('#add-comment').val();
            var comment_picture = $('#id_picture').val();
            if (comment_text == "" && comment_picture == "") {
                alert("Why would you post nothing?");
                return;
            }
            $('#add-comment-submit').hide(300);
            if (comment_picture == "") {
                $.post('/api/new-comment', {
                    'comment_text': comment_text,
                    'comment_picture': comment_picture
                }, function(data) {
                    if (data.is_error) {

                    } else {
                        var el = $(data.comment_html);
                        $('#main-feed').prepend(el);
                        $('#add-comment').val('');
                    }
                });
            } else { document.commentForm.submit(); }
        });

        $('#homepage-loadmore').on('click', function(e) {
            homepage_morefeed();
        });

        homepage_morefeed();

    });
})();
