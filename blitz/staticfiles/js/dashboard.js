'use strict';

(function($) {
    var FEEDITEM_OFFSET = 0;
    var FEED_SCOPE = 'all';
    var FEED_SCOPE_FILTER = 'all';
    var OBJECT_ID;
    var SEARCH_TEXT;
    var CLICKED_FILTER;
    
    // TODO: Watch FEED_SCOPE and OBJECT_ID vars
    var SCOPE_CHANGED = false;
    var SELECTED_ITEM;
    var SELECTED_OBJECT;
    var xhr;

    $(document).ready(function() {
        function homepage_setLoading() {
            $('#homepage-loadmore').hide();
            $('#homepage-loading').show();
        }

        function UpdateViewedFeedsCount(clickedFilter) {
            var clickedFilter = clickedFilter || $('ul.filters.scopes li.active').eq(0) || NaN
            var $FeedItems = $('.feed-item[data-viewed="false"]'),
                unviewedItems = [];

            $.each($FeedItems, function(e) {
                unviewedItems.push({
                    'content_type': $(this).data('content_type'),
                    'object_pk': $(this).data('object_pk')
                })
            });

            if (unviewedItems) {
                $.post('/api/blitz_feed/viewed/mark', {
                    'feed_items': JSON.stringify(unviewedItems)
                }, function(data) {            
                    $FeedItems.attr('data-viewed', 'true');
                });
            }
        }

        function GetViewedFeedsCount() {
            var $feedFilters = $('ul.filters.scopes li.item'),
                filtersData = [];

            $.each($feedFilters, function(e) {
                var filter = $(this);
                filtersData.push({
                    'feed_scope': filter.data('scope'),
                    'object_pk':  filter.data('object-pk')
                });
            });

            $.ajax({
                url: '/api/blitz_feed/count',
                type: 'POST',
                headers:{'filters': JSON.stringify(filtersData)},
                processData: false,
                contentType: false,
            }).then(function(data) {
                $.each(data, function(e) {
                    var filterData = $(this)[0];

                    if (filterData.feed_scope != 'all') {
                        var filter = $('ul.filters.scopes').find('li.item[data-scope='+filterData.feed_scope+']' + '[data-object-pk='+filterData.object_pk+']');
                    } else {
                        var filter = $('ul.filters.scopes').find('li.item[data-scope='+filterData.feed_scope+']');
                    }
                    if (filterData.count < 1) {
                        filter.find('.results-count').hide('fast');
                    } else {
                        filter.find('.results-count').show('fast');
                        filter.find('.results-count .inner').html(filterData.count);
                        // TODO: If '.results-count' don't exists then create the DOM from jQuery
                    }
                });
            });
        }

        function homepage_morefeed(options) {
            var options = options || {};
            var clickedFilter = options.clickedFilter || '';

            homepage_setLoading();
            // Abort ajax requests
            if (xhr) {
                xhr.abort();
            }
            // show alerts on top of All Updates feed
            if (OBJECT_ID === false && FEEDITEM_OFFSET === 0) {
                    $('.alerts-wrapper').removeClass('hidden');
                } 
            xhr = $.get('/api/blitz_feed',
                {'offset': FEEDITEM_OFFSET,
                 'feed_scope': FEED_SCOPE,
                 'feed_scope_filter': FEED_SCOPE_FILTER,
                 'object_id': OBJECT_ID,
                 'search_text': SEARCH_TEXT
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

                    // Mark loaded feed items as viewed
                    UpdateViewedFeedsCount(clickedFilter);

                    // Updates Filters Counter
                    GetViewedFeedsCount();

                    // Enable Post if not "all" scope
                    if (FEED_SCOPE !== 'all') {
                        $postForm.removeClass('hidden');
                        $postFormContainer.append($postForm);
                    }                    
                }
            );
        }


        /**
         * Function which render inbox
         */
        function renderInbox(html) {
            var el = $(html);
            var $inboxContainer = $('.inbox-container');

            $('#main-feed-controls, .formpage-block-form').addClass('hidden');
            $inboxContainer.html(el);
            $inboxContainer.removeClass('hidden');
        }


        /**
         * Function which render summary
         */
        function renderSummary(html) {
            var el = $(html);
            $('#summary').html(el)
                .removeClass('hidden');

            var setWeek = function(weekNum) {
                var selectedWeek = $('.diet-progress .macro-history .week-' + weekNum);
                $('.diet-progress .macro-history .week').not(selectedWeek).addClass('hidden');
                selectedWeek.removeClass('hidden');
            };

            // TODO: Join this two similar events in a single function
            // Filter Diet Goals between Training Days or Resting Days
            $('#summary .switch-training').on('click', function(e) {        
                $(this).addClass('active');
                $('#summary .switch-resting').removeClass('active');
                $('.goals-history .resting').addClass('hidden');
                $('.goals-history .training').removeClass('hidden');
            });

            $('#summary .switch-resting').on('click', function(e) {
                $(this).addClass('active');
                $('#summary .switch-training').removeClass('active');
                $('.goals-history .resting').removeClass('hidden');
                $('.goals-history .training').addClass('hidden');
            });
            // END Filter Diet Goals
            // END TODO

            // Switchs Weeks
            var $weekSelect = $('.diet-progress select');
            $weekSelect.on('change', function(e) {
                var weekNum = $(this).val();
                if (weekNum == 'this_week') {
                    var currentWeek = $('#summary .diet-progress .current').data('week-number');
                    weekNum = currentWeek;
                }
                setWeek(weekNum);
            });

            /**
             * Weeks Switcher - Widget
             */ 
            // Hide <select> element
            $weekSelect.hide();

            // TODO: append widget from jQuery
            var $weekSelectWidget = $('.weekSelector.slide-select');
            var $weekSelectWidgetOptions = $('.weekSelector.slide-select li.item').not('li.arrow'),
                pointer = 0,
                max = $weekSelectWidgetOptions.length-1;

            // When left/righ arrows are clicked
            $weekSelectWidget.on('click', '.right-arrow, .left-arrow', function(e) {
                e.preventDefault();
                var $currentActive = $('.weekSelector.slide-select li.item.active').not('li.arrow');
                if ($currentActive) {
                    // On Right Arrow
                    if ($(this).hasClass('right-arrow')) {
                        if (pointer < max) {
                            pointer+= 1;
                        } else {
                            pointer = 0;
                        }
                    }
                    
                    // On Left Arrow
                    else if ($(this).hasClass('left-arrow')) {
                        if (pointer > 0) {
                            pointer-= 1;
                        } else {
                            pointer = max;
                        }                
                    }

                    // Move to next Option
                    var $nextActive = $weekSelectWidgetOptions.eq(pointer);
                    if ( $nextActive && $nextActive.hasClass('item') && $currentActive.hasClass('item') ) {
                        $nextActive.addClass('active');
                        $currentActive.removeClass('active');

                        // Get next week number
                        var weekNum = $nextActive.data('week-num');

                        // Select next week
                        $('.diet-progress select')
                            .val(weekNum)
                            .trigger('change');
                    }
                } else {
                    $weekSelectWidget
                        .find('li').eq(0)
                            .addClass('active');
                }
            });
        }



        $('.alerts-wrapper').removeClass('hidden');

        var summaryXHR;

        /**
         * Caching DOM Elements
         */
        var $summary = $('#summary'),
            $summarySwitchResting = $('#summary .switch-resting'),
            $mainFeed = $('#main-feed'),
            $feeds = $('.feeds'),
            $inboxContainer = $('.inbox-container'),
            $addCommentSubmit = $('#add-comment-submit'),
            $addComment = $('#add-comment'),
            $searchInput = $('.search-input input'),
            $trainerAlertBox = $('#trainer-alert-box'),
            $alertsCount = $('li[data-scope=alerts] .results-count .inner'),
            $postFormContainer = $('#add-comment-container'),
            $postForm = $('#add-comment-container form');

        // Removes Post Form (will be added when the selected filter is not "All Updates")
        var removePostForm = function() {
            $postFormContainer.empty();
        }
        removePostForm();

        var reduceAlertsCount = function() {
            $alertsCount.html( $alertsCount.html()-1 );
        }

        // Add comment button show/hide
        $addComment.on('focus', function() {
            $addCommentSubmit.show(300);
        });
        $addComment.on('blur', function() {
            if ($(this).val() === "") {
                $addCommentSubmit.hide(300);
            }
        });

        // Add comment submit
        $addCommentSubmit.on('click', function(e) {
            e.preventDefault();
            var comment_text = $addComment.val();
            if (comment_text === "") {
                alert("Why would you post nothing?");
                return;
            }
            $addCommentSubmit.hide(300);

            if (SELECTED_ITEM === 'invitee') {
                 alert("This feed will be happening once the client signs up");
            } else {
                $.post('/api/new-comment', {
                    'comment_text': comment_text,
                    'object_id': OBJECT_ID,
                    'selected_item': SELECTED_ITEM
                }, function(data) {
                    if (data.is_error) {

                    } else {
                        var el = $(data.comment_html);
                        $mainFeed.prepend(el);
                        $addComment.val('');
                    }
                });
            }
        });


        // On Windows Resize
        $(window).resize(function() {
            $('.feeds').width( $('.content-wrapper').width()-(330+35) );
        });
        $(window).trigger('resize');
        // END

        $('#homepage-loadmore').on('click', function(e) {
            homepage_morefeed({clickedFilter: CLICKED_FILTER});
        });

        // Search
        var $clientGroupFilters = $('.filters li.solo-client, li.blitz');
        $searchInput.on('input', function(e) {
            var searchText = $(this).val();
            $.each($clientGroupFilters, function(index, value) {
                if ( $(this).text().trim().toLowerCase().indexOf(searchText.toLowerCase()) === -1 ) {
                    $(this).hide();
                } else {
                    $(this).show();
                }
            });
        });

        $searchInput.keypress(function(e) {
            var searchText = $(this).val();
            if (searchText) {
                if (e.which == 13) {
                    SEARCH_TEXT = searchText;
                    FEEDITEM_OFFSET = 0;
                    FEED_SCOPE = 'all';
                    OBJECT_ID = '';

                    // Clear feed container
                    if ( $mainFeed.html() ) {
                        $mainFeed.empty();
                    }

                    if ( $inboxContainer.html() ) {
                        $inboxContainer.empty();
                    }
                    // Abort ajax requests
                    if (xhr) {
                        xhr.abort();
                    }

                    if (summaryXHR) {
                        summaryXHR.abort();
                    }
                    homepage_morefeed();
                }
            }
        });


        /**
         * Trainer Alerts
         */ 
        $trainerAlertBox.on('click', 'button[data-action=leave-message]', function(e) {
            var targetId = $(this).data('target-id')
                MessageForm = $('#'+targetId).find('form'),
                toggleButton = $(this);

            // Hide unfocused message box
            $('button[data-action=leave-message]').not( toggleButton )
                .html('Message');

            $('.message-entry').not( $('#'+targetId) )
                .addClass('hidden')
                .find('textarea')
                    .val('');

            // Shows textarea for type a message
            if ( $('#'+targetId).hasClass('hidden') ) {
                // Showing textarea
                $('#'+targetId).removeClass('hidden');
                $(this).html('Close');
            } else {
                $('#'+targetId).addClass('hidden');
                $(this).html('Message');
            }
        });

        // Reduce Alerts count on dismiss
        $trainerAlertBox.on('click', '.dismiss-alert', function(e) {
            reduceAlertsCount();
        })

        // On Click Send Message Button
        $('.message-entry form').submit(function(e) {
            e.preventDefault();

            var $form = $(this),
                $submitButton = $form.find('button[type="submit"]'),
                formData = new FormData( this );
            
                $submitButton.hide();

            // Submit form via AJAX
            var hrx = $.ajax({
                url: $(this).attr('action'),
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false
            }).then(function(data) {
                reduceAlertsCount();
                $form.parent().hide();
                $.ajax({
                    url: '/trainer/dismiss-alert',
                    type: 'POST',
                    data:{alert_pk: $form.data('alert_pk')},
                    alert_pk: $form.data('alert_pk')
                }).then(function(data) {
                    $form.closest('.trainer-alert')
                        .fadeOut(500);
                }, function(error) {
                    // TODO: Show alert in the UI instead of built-in alert
                    alert(error)
                    $form.parent().show();
                });
            }, function(error) {
                // TODO: Show alert in the UI browser built-in alert
                $submitButton.show();
                alert( JSON.stringify(error) );
            });
        });
        // END Trainer alerts


        /**
         * Filters
         */ 
        $('.filters, .feeds-filter').on('click', 'li', function(event) {
            // ScrollUp to very top
            $(document).scrollTop(0);

            // Detects Changes
            // TODO: Watch FEED_SCOPE and OBJECT_ID vars
            if ( $(this).data('scope') && ( FEED_SCOPE !== $(this).data('scope') ) ) {
                SCOPE_CHANGED = true;
            } else {
                SCOPE_CHANGED = false;
            }
            // END

            var $clickedFilter = $(this),
                unviewedItemsCount = $clickedFilter.find('.results-count .inner').html();

            // Abort pending ajax requests
            if (xhr) {
                xhr.abort();
            }

            if (summaryXHR) {
                summaryXHR.abort();
            }

            FEEDITEM_OFFSET = 0;
            FEED_SCOPE = $(this).data('scope') || FEED_SCOPE;
            FEED_SCOPE_FILTER = $(this).data('scope-filter') || FEED_SCOPE_FILTER;

            // On Scope Change (when a left-sidebar filter is clicked)
            if ($(this).parent().hasClass('scopes')) {
                OBJECT_ID = $(this).data('object-pk') || false;
                FEED_SCOPE_FILTER = 'all'

                $('.feeds-filter ul li').not($(this)).removeClass('active');
                $('.feeds-filter ul li:first-child').addClass('active');

                // Make it Global
                CLICKED_FILTER = $clickedFilter;
            } else {
                CLICKED_FILTER = NaN;
            }

            SEARCH_TEXT = '';

            // Hide and clear client summary
            $summary.empty();
            // END

            // Clear feed container
            var clearFeed = function() {
                if ( $mainFeed.html() ) {
                    $mainFeed.empty();
                }
                if ( $inboxContainer.html() ) {
                    $inboxContainer.empty();
                }
                $('.feeds-filter').removeClass('hidden');
                $('#main-feed-controls, .formpage-block-form').removeClass('hidden');
            }
            clearFeed();
            // END

            // Hide and clear blitz group header
            if (SCOPE_CHANGED == true ) {
                $('.group').empty();
            }        
            // END

            // Hide Alerts
            $('.alerts-wrapper').addClass('hidden');
            // END

            SELECTED_ITEM = '';
            SELECTED_OBJECT = 0;
            if (FEED_SCOPE === 'all') {
                OBJECT_ID = false;
                // Reset Search Input
                $searchInput.val('')
                    .trigger('input');
                homepage_morefeed({clickedFilter: CLICKED_FILTER});
                
                // Removes New Post Form
                removePostForm();
            } else if (FEED_SCOPE === 'alerts') { // Alerts
                $('#main-feed-controls, .formpage-block-form').addClass('hidden');
                $('.feeds-filter').addClass('hidden');
                $('.alerts-wrapper').removeClass('hidden');
            } else {
                // Inbox
                if (FEED_SCOPE === 'inbox') {
                    // Reset Seearch Input
                    $searchInput.val('')
                        .trigger('input');
                    $.get('/api/inbox_feed', function(data) {
                        renderInbox(data.html);
                    });
                }
                else {
                    $inboxContainer.addClass('hidden');
                }

                // Blitz
                if (FEED_SCOPE === 'blitz') {
                    SELECTED_ITEM = 'blitz';
                    $.get('/api/blitz/' + OBJECT_ID, function(data) {
                        $('.group').html(data.html);                
                    });
                }

                // Client
                if (FEED_SCOPE === 'client') {
                    SELECTED_ITEM = 'client';
                    if (OBJECT_ID) {
                        summaryXHR = $.get('/api/client_summary/' + OBJECT_ID, function(data) {
                            renderSummary(data.html);
                        });
                    }
                } else {
                    $summary.empty();
                }

                // Invitee
                if (FEED_SCOPE === 'invitee') {
                    if (OBJECT_ID) {
                        SELECTED_ITEM = 'invitee';
                        summaryXHR = $.get('/api/invitee_summary/' + OBJECT_ID, function(data) {
                            renderSummary(data.html);
                        });
                    }
                } else {
                    $summary.empty();
                }

                homepage_morefeed({clickedFilter: CLICKED_FILTER});
            }

            // Sets 'active' class to clicked filter
            $(this).parent().find('li').not($(this))
                .removeClass('active');
            $(this).addClass('active');
        });
        // End Filters

        homepage_morefeed();
    });
})(jQuery);
