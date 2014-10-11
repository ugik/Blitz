var FEEDITEM_OFFSET = 0;
var FEED_SCOPE = 'all';
var OBJECT_ID = '';

function homepage_setLoading() {
    $('#homepage-loadmore').hide();
    $('#homepage-loading').show();
}

function homepage_morefeed() {
    homepage_setLoading();
    $.get('/api/blitz_feed',
        {'offset': FEEDITEM_OFFSET,
         'feed_scope': FEED_SCOPE,
         'object_id': OBJECT_ID
        },
        function(data) {
            for (var i=0; i<data.feeditems.length; i++) {
                var item = data.feeditems[i];
                var el = $(item.html);
                $('#main-feed').append(el);
            }
            FEEDITEM_OFFSET = data.offset;
            $('#homepage-loadmore').show();
            $('#homepage-loading').hide();
        }
    );
}


$(document).ready(function() {

    // add comment button show/hide
    $('#add-comment').on('focus', function() {
        $('#add-comment-submit').show(300);
    });
    $('#add-comment').on('blur', function() {
        if ($(this).val() === "") {
            $('#add-comment-submit').hide(300);
        }
    });

    // add comment submit
    $('#add-comment-submit').on('click', function(e) {
        e.preventDefault();
        var comment_text = $('#add-comment').val();
        if (comment_text === "") {
            alert("Why would you post nothing?");
            return;
        }
        $('#add-comment-submit').hide(300);
        $.post('/api/new-comment', {
            'comment_text': comment_text,
        }, function(data) {
            if (data.is_error) {

            } else {
                var el = $(data.comment_html);
                $('#main-feed').prepend(el);
                $('#add-comment').val('');
            }
        });
    });

    $('#homepage-loadmore').on('click', function(e) {
        homepage_morefeed();
    });

    // Filters
    $('.filters').on('click', 'li', function(event) {
        FEEDITEM_OFFSET = 0;
        FEED_SCOPE = $(this).data('scope') || FEED_SCOPE;
        OBJECT_ID = $(this).data('object-pk') || false;

        // Hide and clear client summary
        $('#summary').addClass('hidden').html('');

        // Clear feed container
        if ( $('#main-feed').html() ) {
            $('#main-feed').html('');
        }
        $('#main-feed-controls, .formpage-block-form').removeClass('hidden');
        
        if (FEED_SCOPE === 'all') {
            homepage_morefeed();
            OBJECT_ID = false;
        } else {
            if (FEED_SCOPE === 'inbox') {
                $.get('/api/inbox_feed', function(data) {
                    var el = $(data.html);
                    $('#main-feed-controls, .formpage-block-form').addClass('hidden');
                    if ( $('.inbox-container').length == 0 ) {
                        $('.feeds').append('<div class="inbox-container">Inserted</div>');
                    }
                    $('.inbox-container').html(el);
                });
            }

            if (FEED_SCOPE === 'client') {
                if (OBJECT_ID) {
                    // var client = window.CLIENTS.filter(function(e){return e.id == OBJECT_ID;})[0];
                    $.get('/api/client_summary/' + OBJECT_ID, function(data) {
                        var el = $(data.html);
                        
                        $('#summary').html(el);
                        $('#summary').removeClass('hidden');

                        var setWeek = function(weekNum) {
                            var selectedWeek = $('.diet-progress .macro-history .week-' + weekNum);
                            $('.diet-progress .macro-history .week').not(selectedWeek).addClass('hidden');
                            selectedWeek.removeClass('hidden');
                        };

                        // TODO: Join this two similar events in a single function
                        // Filter Diet Goals between Training Days or Resting Days
                        $('#summary .switch-training').on('click', function(e) {
                            $(this).addClass('btn-default');
                            $(this).removeClass('btn-link');

                            $('#summary .switch-resting').removeClass('btn-default');
                            $('#summary .switch-resting').addClass('btn-link');

                            $('.goals-history .resting').addClass('hidden');
                            $('.goals-history .training').removeClass('hidden');
                        });

                        $('#summary .switch-resting').on('click', function(e) {
                            $(this).addClass('btn-default');
                            $(this).removeClass('btn-link');

                            $('#summary .switch-training').removeClass('btn-default');
                            $('#summary .switch-training').addClass('btn-link');

                            $('.goals-history .resting').removeClass('hidden');
                            $('.goals-history .training').addClass('hidden');
                        });
                        // END Filter Diet Goals
                        // END TODO

                        // Switchs Week
                        $('.diet-progress select').on('change', function(e) {
                            var weekNum = $(this).val();
                            if (weekNum == 'this_week') {
                                var currentWeek = $('#summary .diet-progress .current').data('week-number');
                                weekNum = currentWeek;
                            }
                            setWeek(weekNum);
                        });
                    });
                }
            } else {
                $('#summary').addClass('hidden');
            }
            homepage_morefeed();
        }

        // Sets 'active' class to clicked filter
        $('ul.filters li').removeClass('active');
        $(this).addClass('active');
    });
    // End Filters

    homepage_morefeed();
});
