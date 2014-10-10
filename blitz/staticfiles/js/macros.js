$(document).ready(function() {

    var MacroDay = Backbone.Model.extend({

    });

    var MacroCalendarView = Backbone.View.extend({

        template: _.template($('#tpl-macro-calendar-view').html()),

        initialize: function() {
            this.week_macros = this.options.week_macros;
        },

        render: function() {
            var that = this;
            $(this.el).html(this.template({
                week_macros: that.week_macros,
			}));
			return this;
        },

    });

    var MacroDayView = Backbone.View.extend({

        template: _.template($('#tpl-macro-day-view').html()),

        initialize: function() {
            this.macro = this.options.macro;
        },

        events: {
            "click .goback": "goBack",
            "click .goforward": "goForward",
            "click .undo": "undo",
            "click .choice": "newChoice",
            "click .choice-icon": "choiceI",
        },

        render: function() {
            var that = this;
            $(this.el).html(this.template({
                macro: that.macro,
			}));
			return this;
        },

        goBack: function() {
            this.trigger('goback');
        },

        goForward: function() {
            this.trigger('goforward');
        },

        setLoading: function() {
           // TODO
        },

        setLoaded: function() {
           // TODO
        },

        undo: function() {
            this.trigger('undo');
        },

        isComplete: function() {
            return this.$('.choice.selected').size() == 4;
        },

        hideForward: function() {
            this.$('.goforward').hide();
        },

        hideBack: function() {
            this.$('.goback').hide();
        },

        getDetails: function() {
            return {
                'calories': this.$('.choice-yes[data-slug="calories"]').hasClass('selected') ? 'yes' : 'no',
                'protein': this.$('.choice-yes[data-slug="protein"]').hasClass('selected') ? 'yes' : 'no',
                'carbs': this.$('.choice-yes[data-slug="carbs"]').hasClass('selected') ? 'yes' : 'no',
                'fat': this.$('.choice-yes[data-slug="fat"]').hasClass('selected') ? 'yes' : 'no',
            }
        },

        newChoice: function(event) {
            var target = $(event.target);
            var slug = target.data('slug');
            this.$('.choice[data-slug="' + slug + '"]').removeClass('selected');
            target.addClass('selected');
            if (this.isComplete()) {
                var macro = this.getDetails();
                this.trigger('savemacro', macro);
            }
        },

        choiceI: function(e) {
            e.preventDefault();
            e.stopPropagation();
            $(e.target).parent().click();
        }

    });

    var MacroWeekView = Backbone.View.extend({

        template: _.template($('#tpl-macro-week-view').html()),

        initialize: function() {
            this.week_macros = this.options.week_macros;
            this.current_day_index = this.options.current_day_index;
            this.current_week = this.options.current_week;
        },

        render: function() {
            var that = this;
            $(this.el).html(this.template({

			}));
            this.calendar = new MacroCalendarView({week_macros: that.week_macros});
            this.$('.calendar-container').html(this.calendar.render().el);
            this.showDay(that.current_day_index);
			return this;
        },

        showDay: function(day_index) {
            var that = this;
            that.current_day_index = day_index;
            var macro = this.week_macros[day_index];
            var day_view = new MacroDayView({ macro: macro });

            day_view.on('goback', that.goBack, that);
            day_view.on('goforward', that.goForward, that);
            day_view.on('undo', that.undo, that);
            day_view.on('savemacro', that.saveMacro, that);

            that.day_view = day_view;

            if (macro.has_entry) this.showCalendar();
            else this.hideCalendar();

            this.$('.day-view-container').html(day_view.render().el);

            if (this.current_day_index == CURRENT_DAY_INDEX && this.current_week == CURRENT_WEEK) day_view.hideForward();
            if (this.current_day_index == 0 && this.current_week == 1) day_view.hideBack();

        },

        goBack: function() {
            if (this.current_day_index > 0) {
                var new_index = this.current_day_index - 1;
                this.showDay(new_index);
            } else {
                if (this.current_week > 1) {
                    this.current_week -= 1;
                    getWeek(this.current_week, 6);
                }
            }
        },

        goForward: function() {
            if (this.current_day_index < 6) {
                var new_index = this.current_day_index + 1;
                this.showDay(new_index);
            } else {
                if (this.current_week < CURRENT_WEEK) {
                    this.current_week += 1;
                    getWeek(this.current_week, 0);
                }
            }
        },

        undo: function() {
            var that = this;
            var macro = this.week_macros[this.current_day_index];
            $.post('/macros/undo-day', {
                week: macro.week,
                day_index: macro.day_index,
            }, function(data) {
                // TODO: should be backbone model update instead
                that.week_macros[that.current_day_index] = data;
                that.render();
            });
        },

        saveMacro: function(details) {
            var that = this;
            var macro = this.week_macros[this.current_day_index];
            $.post('/macros/save-day', {
                week: macro.week,
                day_index: macro.day_index,
                calories: details.calories,
                protein: details.protein,
                fat: details.fat,
                carbs: details.carbs,
            }, function(data) {
                // TODO: should be backbone model update instead
                that.week_macros[that.current_day_index] = data;
                that.render();
            });
        },

        hideCalendar: function() {
            this.$('.calendar-container').hide();
        },

        showCalendar: function() {
            this.$('.calendar-container').show();
        },

    });


    window.getWeek = function(week, day_index) {
        $.get('/macros/get-macros-for-blitz-week', {week: week}, function(data) {
            var view = new MacroWeekView({
                week_macros: data.week_macros,
                current_day_index: day_index,
                current_week: week,
            });
            $('#macro-block-container').html(view.render().el);
        });
    }

    getWeek(CURRENT_WEEK, CURRENT_DAY_INDEX);

});