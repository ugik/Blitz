
$(document).ready(function() {
    // expanding textareas
    $(document).on('DOMSubtreeModified', function() {
        $('.add-child-comment-container textarea').expandingTextarea().css('position', 'relative');
    });

    // todo: abstract here
    function focusAddChildComment(content_type, object_pk) {

    }

    function unfocusAddChildComment(content_type, object_pk) {

    }

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
