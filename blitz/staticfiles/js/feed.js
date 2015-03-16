'use strict';

(function(){
    jQuery(document).ready(function($) {
        // expanding textareas
        $(document).on('DOMSubtreeModified', function() {
           $('.add-child-comment-container textarea').expandingTextarea();
        });

        // todo: abstract here
        function focusAddChildComment(content_type, object_pk) {

        }

        function unfocusAddChildComment(content_type, object_pk) {

        }

        // Hack to Fix Exercice Matrix borders
        // TODO: Make it happen just with HTML and CSS, without javascript help

        window.fixExerciseMatrixBorders = function fixExerciseMatrixBorders(containerHTML) {
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

        $.each($('.profile-gym-session'), function(e) {
            fixExerciseMatrixBorders($(this));
        });


        // add child comment button show/hide
        $(document).on('focus', '.add-child-comment-textarea', function(event) {
            var parent = $(event.target).closest('.add-child-comment-container');
            parent.find('.add-child-comment-submit').show(300)
        });
        $(document).on('blur', '.add-child-comment-textarea', function(event) {
            if ($(this).val() == "") {
                var parent = $(event.target).closest('.add-child-comment-container');
                parent.find('.add-child-comment-submit').hide(300)
            }
        });


        // add child comment submit
        $(document).on('click', '.add-child-comment-submit', function(event) {
            var parent = $(event.target).closest('.add-child-comment-container');
            var footer = $(this).closest('.feed-item-footer');
            var content_type=footer.data('content_type');
            var object_pk=footer.data('object_pk');
            $(this).hide(300);
            $.post('/api/new-child-comment', {
                'comment_text': parent.find('.add-child-comment-textarea').val(),
                'content_type': content_type,
                'object_pk': object_pk,
            }, function(data) {
                if (data.is_error) {

                } else {
                    footer.replaceWith($(data.html).find('.feed-item-footer'));
                }
            });
        });


        // "comment" button on feed item (gym session or parent comment)
        $(document).on('click', '.feeditem-actions-container .comment-link', function(e) {
            var footer = $(this).closest('.feed-item-footer');
            var content_type = footer.data('content_type');
            var object_pk = footer.data('object_pk');
            footer.find('.add-child-comment-textarea').focus();
            footer.find('.add-child-comment-submit').show(300);
        });

        // "like" button on feed item
        $(document).on('click', '.feeditem-actions-container .like-link', function(e) {
            var footer = $(this).closest('.feed-item-footer');
            var content_type = footer.data('content_type');
            var object_pk = footer.data('object_pk');
            if (content_type == "comment") {
                $.post('/api/comment_like',
                    {'comment_pk': object_pk},
                    function(data) {
                        if (data.is_error) {

                        } else {
                            footer.replaceWith($(data.html).find('.feed-item-footer'));
                        }
                    }
                );
            }
            else if (content_type == "check in") {
                $.post('/api/checkin_like',
                    {'checkin_pk': object_pk},
                    function(data) {
                        if (data.is_error) {

                        } else {
                            footer.replaceWith($(data.html).find('.feed-item-footer'));
                        }
                    }
                );
            }
            else if (content_type == "gym session") {
                $.post('/api/gym_session_like',
                    {'gym_session_pk': object_pk},
                    function(data) {
                        if (data.is_error) {

                        } else {
                            footer.replaceWith($(data.html).find('.feed-item-footer'));
                        }
                    }
                );
            }

        });

        // Unlike
        $(document).on('click', '.feeditem-actions-container .unlike-link', function(e) {
            var footer = $(this).closest('.feed-item-footer');
            var content_type = footer.data('content_type');
            var object_pk = footer.data('object_pk');
            if (content_type == "comment") {
                $.post('/api/comment_unlike',
                    {'comment_pk': object_pk},
                    function(data) {
                        if (data.is_error) {

                        } else {
                            footer.replaceWith($(data.html).find('.feed-item-footer'));
                        }
                    }
                );
            }
            else if (content_type == "check in") {
                $.post('/api/checkin_unlike',
                    {'checkin_pk': object_pk},
                    function(data) {
                        if (data.is_error) {

                        } else {
                            footer.replaceWith($(data.html).find('.feed-item-footer'));
                        }
                    }
                );
            }
            else if (content_type == "gym session") {
                $.post('/api/gym_session_unlike',
                    {'gym_session_pk': object_pk},
                    function(data) {
                        if (data.is_error) {

                        } else {
                            footer.replaceWith($(data.html).find('.feed-item-footer'));
                        }
                    }
                );
            }

        });

        // Like on child comment
        $(document).on('click', '.child-comment .like-link', function(e) {
            var footer = $(this).closest('.feed-item-footer');
            var childComment = $(this).closest('.child-comment');
            var content_type = "comment";
            var object_pk = childComment.data('object_pk');

            $.post('/api/comment_like',
                {'comment_pk': object_pk},
                function(data) {
                    if (data.is_error) {

                    } else {
                        footer.replaceWith($(data.html).find('.feed-item-footer'));
                    }
                }
            );
        });

        // Unlike child comment
        $(document).on('click', '.child-comment .unlike-link', function(e) {

            var footer = $(this).closest('.feed-item-footer');
            var childComment = $(this).closest('.child-comment');
            var content_type = "comment";
            var object_pk = childComment.data('object_pk');

            $.post('/api/comment_unlike',
                {'comment_pk': object_pk},
                function(data) {
                    if (data.is_error) {

                    } else {
                        footer.replaceWith($(data.html).find('.feed-item-footer'));
                    }
                }
            );
        });

        // Child comment tooltip
        $(document).on('mouseover', '.child-comment .num-likes', function(e) {
            $(this).tooltip('show');
        });
        $(document).on('mouseout', '.child-comment .num-likes', function(e) {
            $(this).tooltip('hide');
        });

    });
})();
