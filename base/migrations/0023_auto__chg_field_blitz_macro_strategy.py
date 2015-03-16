# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Blitz.macro_strategy'
        db.alter_column(u'base_blitz', 'macro_strategy', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):

        # Changing field 'Blitz.macro_strategy'
        db.alter_column(u'base_blitz', 'macro_strategy', self.gf('django.db.models.fields.CharField')(max_length=1))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'base.blitz': {
            'Meta': {'object_name': 'Blitz'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'custom_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'custom_price_per_workout': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macro_strategy': ('django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '10'}),
            'marketplace': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'price_model': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1', 'blank': 'True'}),
            'provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recurring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sales_page_content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.SalesPageContent']", 'null': 'True'}),
            'sample': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_expect_text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'trainer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Trainer']"}),
            'url_slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'}),
            'uses_macros': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'workout_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutPlan']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'base.blitzinvitation': {
            'Meta': {'object_name': 'BlitzInvitation'},
            'blitz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Blitz']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macro_formula': ('django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '10'}),
            'macro_target_json': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'signup_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'workout_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutPlan']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'base.blitzmember': {
            'Meta': {'object_name': 'BlitzMember'},
            'blitz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Blitz']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        },
        u'base.checkin': {
            'Meta': {'object_name': 'CheckIn'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'db_index': 'True'}),
            'front_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'side_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'base.checkinlike': {
            'Meta': {'object_name': 'CheckInLike'},
            'checkin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.CheckIn']", 'null': 'True', 'blank': 'True'}),
            'date_and_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'base.client': {
            'Meta': {'object_name': 'Client'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'balanced_account_uri': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'external_headshot_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'forgot_password_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1', 'blank': 'True'}),
            'has_completed_intro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'height_feet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'height_inches': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macro_target_json': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'US/Pacific'", 'max_length': '40'}),
            'units': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'weight_in_lbs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'base.comment': {
            'Meta': {'object_name': 'Comment'},
            'checkin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'checkincomments'", 'null': 'True', 'to': u"orm['base.CheckIn']"}),
            'date_and_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'gym_session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gymsessioncomments'", 'null': 'True', 'to': u"orm['base.GymSession']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'parent_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Comment']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'base.commentlike': {
            'Meta': {'object_name': 'CommentLike'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Comment']", 'null': 'True', 'blank': 'True'}),
            'date_and_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'base.completedset': {
            'Meta': {'object_name': 'CompletedSet'},
            'gym_session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.GymSession']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_reps_completed': ('django.db.models.fields.IntegerField', [], {}),
            'set_type': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'weight_in_lbs': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'workout_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutSet']"})
        },
        u'base.feeditem': {
            'Meta': {'object_name': 'FeedItem'},
            'blitz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Blitz']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        u'base.gymsession': {
            'Meta': {'object_name': 'GymSession'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_of_session': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_logged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'workout_plan_day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutPlanDay']"})
        },
        u'base.gymsessionlike': {
            'Meta': {'object_name': 'GymSessionLike'},
            'date_and_time': ('django.db.models.fields.DateTimeField', [], {}),
            'gym_session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.GymSession']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'base.heading': {
            'Meta': {'object_name': 'Heading'},
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'saying': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'base.macroday': {
            'Meta': {'object_name': 'MacroDay'},
            'calories': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'carbs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'day': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'fat': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'base.salespagecontent': {
            'Meta': {'object_name': 'SalesPageContent'},
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_ditch_1': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'last_ditch_2': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'program_introduction': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'program_last_words': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'program_title': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'program_who': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'program_why': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'sales_page_key': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'social_proof_header_html': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'testimonial_1_name': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'testimonial_1_text': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'testimonial_2_name': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'testimonial_2_text': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'testimonial_3_name': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'testimonial_3_text': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'trainer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Trainer']", 'null': 'True'}),
            'trainer_headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'trainer_note': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'trainer_signature': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url_slug': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'video_html': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
        },
        u'base.scout': {
            'Meta': {'object_name': 'Scout'},
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'url_slug': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5'})
        },
        u'base.trainer': {
            'Meta': {'object_name': 'Trainer'},
            'currently_viewing_blitz': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'currently_viewing_trainer'", 'null': 'True', 'to': u"orm['base.Blitz']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'external_headshot_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'forgot_password_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'payment_info': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'referral': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Scout']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'US/Pacific'", 'max_length': '40'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'base.traineralert': {
            'Meta': {'object_name': 'TrainerAlert'},
            'alert_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'trainer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Trainer']"}),
            'trainer_dismissed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'workout_plan_day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutPlanDay']", 'null': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'workouts.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Lift']"}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'sets_display': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'workout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Workout']"})
        },
        u'workouts.lift': {
            'Meta': {'object_name': 'Lift'},
            'allow_weight_or_body': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lift_type': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'weight_or_body': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'workouts.workout': {
            'Meta': {'object_name': 'Workout'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sets_grouped': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        u'workouts.workoutplan': {
            'Meta': {'object_name': 'WorkoutPlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'trainer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Trainer']", 'null': 'True'})
        },
        u'workouts.workoutplanday': {
            'Meta': {'object_name': 'WorkoutPlanDay'},
            'day_index': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'day_of_week': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Workout']"}),
            'workout_plan_week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutPlanWeek']"})
        },
        u'workouts.workoutplanweek': {
            'Meta': {'object_name': 'WorkoutPlanWeek'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'week': ('django.db.models.fields.IntegerField', [], {}),
            'workout_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutPlan']"})
        },
        u'workouts.workoutset': {
            'Meta': {'object_name': 'WorkoutSet'},
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Exercise']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Lift']"}),
            'num_reps': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'workout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Workout']"})
        }
    }

    complete_apps = ['base']