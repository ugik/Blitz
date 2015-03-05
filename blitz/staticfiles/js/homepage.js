'use strict';

(function() {
    var FEEDITEM_OFFSET = 0;

    jQuery(document).ready(function($) {
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
