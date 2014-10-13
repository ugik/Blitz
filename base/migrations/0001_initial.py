# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trainer'
        db.create_table(u'base_trainer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('headshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('external_headshot_url', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='US/Pacific', max_length=40)),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('forgot_password_token', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('currently_viewing_blitz', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='currently_viewing_trainer', null=True, to=orm['base.Blitz'])),
        ))
        db.send_create_signal(u'base', ['Trainer'])

        # Adding model 'Client'
        db.create_table(u'base_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('weight_in_lbs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height_feet', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height_inches', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='U', max_length=1, blank=True)),
            ('headshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('external_headshot_url', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='US/Pacific', max_length=40)),
            ('has_completed_intro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('macro_target_json', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('forgot_password_token', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('units', self.gf('django.db.models.fields.CharField')(default='I', max_length=1, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('balanced_account_uri', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
        ))
        db.send_create_signal(u'base', ['Client'])

        # Adding model 'Blitz'
        db.create_table(u'base_blitz', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=25)),
            ('trainer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Trainer'])),
            ('recurring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provisional', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sales_page_content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.SalesPageContent'], null=True)),
            ('workout_plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.WorkoutPlan'], null=True, blank=True)),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('custom_end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('custom_price_per_workout', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('to_expect_text', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('uses_macros', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('macro_strategy', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('price', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('price_model', self.gf('django.db.models.fields.CharField')(default='R', max_length=1, blank=True)),
        ))
        db.send_create_signal(u'base', ['Blitz'])

        # Adding model 'BlitzInvitation'
        db.create_table(u'base_blitzinvitation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blitz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Blitz'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('signup_key', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
        ))
        db.send_create_signal(u'base', ['BlitzInvitation'])

        # Adding model 'BlitzMember'
        db.create_table(u'base_blitzmember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Client'])),
            ('blitz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Blitz'])),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'base', ['BlitzMember'])

        # Adding model 'FeedItem'
        db.create_table(u'base_feeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blitz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Blitz'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'base', ['FeedItem'])

        # Adding model 'GymSession'
        db.create_table(u'base_gymsession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_session', self.gf('django.db.models.fields.DateField')()),
            ('workout_plan_day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.WorkoutPlanDay'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Client'])),
            ('notes', self.gf('django.db.models.fields.TextField')(default='')),
            ('is_logged', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'base', ['GymSession'])

        # Adding model 'CompletedSet'
        db.create_table(u'base_completedset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gym_session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.GymSession'])),
            ('workout_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.WorkoutSet'])),
            ('num_reps_completed', self.gf('django.db.models.fields.IntegerField')()),
            ('weight_in_lbs', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('set_type', self.gf('django.db.models.fields.CharField')(default='S', max_length=1)),
        ))
        db.send_create_signal(u'base', ['CompletedSet'])

        # Adding model 'CheckIn'
        db.create_table(u'base_checkin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Client'])),
            ('weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('front_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('side_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'base', ['CheckIn'])

        # Adding model 'Comment'
        db.create_table(u'base_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_and_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('parent_comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Comment'], null=True, blank=True)),
            ('gym_session', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gymsessioncomments', null=True, to=orm['base.GymSession'])),
        ))
        db.send_create_signal(u'base', ['Comment'])

        # Adding model 'CommentLike'
        db.create_table(u'base_commentlike', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Comment'], null=True, blank=True)),
            ('date_and_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'base', ['CommentLike'])

        # Adding model 'GymSessionLike'
        db.create_table(u'base_gymsessionlike', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('gym_session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.GymSession'], null=True, blank=True)),
            ('date_and_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'base', ['GymSessionLike'])

        # Adding model 'MacroDay'
        db.create_table(u'base_macroday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Client'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('protein', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('carbs', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('fat', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('calories', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['MacroDay'])

        # Adding model 'TrainerAlert'
        db.create_table(u'base_traineralert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alert_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('trainer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Trainer'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Client'])),
            ('date_created', self.gf('django.db.models.fields.DateField')()),
            ('trainer_dismissed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('workout_plan_day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.WorkoutPlanDay'], null=True)),
        ))
        db.send_create_signal(u'base', ['TrainerAlert'])

        # Adding model 'SalesPageContent'
        db.create_table(u'base_salespagecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trainer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Trainer'], null=True)),
            ('group', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=140, null=True, blank=True)),
            ('url_slug', self.gf('django.db.models.fields.CharField')(default='', max_length=30, null=True, blank=True)),
            ('sales_page_key', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('trainer_headshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('program_title', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('program_introduction', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('program_why', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('program_who', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('program_last_words', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('trainer_note', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('trainer_signature', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('video_html', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('social_proof_header_html', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('testimonial_1_text', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('testimonial_1_name', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('testimonial_2_text', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('testimonial_2_name', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('testimonial_3_text', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('testimonial_3_name', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('last_ditch_1', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('last_ditch_2', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['SalesPageContent'])

        # Adding model 'Heading'
        db.create_table(u'base_heading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('heading_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['Heading'])


    def backwards(self, orm):
        # Deleting model 'Trainer'
        db.delete_table(u'base_trainer')

        # Deleting model 'Client'
        db.delete_table(u'base_client')

        # Deleting model 'Blitz'
        db.delete_table(u'base_blitz')

        # Deleting model 'BlitzInvitation'
        db.delete_table(u'base_blitzinvitation')

        # Deleting model 'BlitzMember'
        db.delete_table(u'base_blitzmember')

        # Deleting model 'FeedItem'
        db.delete_table(u'base_feeditem')

        # Deleting model 'GymSession'
        db.delete_table(u'base_gymsession')

        # Deleting model 'CompletedSet'
        db.delete_table(u'base_completedset')

        # Deleting model 'CheckIn'
        db.delete_table(u'base_checkin')

        # Deleting model 'Comment'
        db.delete_table(u'base_comment')

        # Deleting model 'CommentLike'
        db.delete_table(u'base_commentlike')

        # Deleting model 'GymSessionLike'
        db.delete_table(u'base_gymsessionlike')

        # Deleting model 'MacroDay'
        db.delete_table(u'base_macroday')

        # Deleting model 'TrainerAlert'
        db.delete_table(u'base_traineralert')

        # Deleting model 'SalesPageContent'
        db.delete_table(u'base_salespagecontent')

        # Deleting model 'Heading'
        db.delete_table(u'base_heading')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macro_strategy': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price_model': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1', 'blank': 'True'}),
            'provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recurring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sales_page_content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.SalesPageContent']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_expect_text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'trainer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Trainer']"}),
            'url_slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '25'}),
            'uses_macros': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'workout_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutPlan']", 'null': 'True', 'blank': 'True'})
        },
        u'base.blitzinvitation': {
            'Meta': {'object_name': 'BlitzInvitation'},
            'blitz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Blitz']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'signup_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'base.blitzmember': {
            'Meta': {'object_name': 'BlitzMember'},
            'blitz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Blitz']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base.checkin': {
            'Meta': {'object_name': 'CheckIn'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'front_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'side_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'date_and_time': ('django.db.models.fields.DateTimeField', [], {}),
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
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'base.gymsession': {
            'Meta': {'object_name': 'GymSession'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_of_session': ('django.db.models.fields.DateField', [], {}),
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
            'heading_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'base.macroday': {
            'Meta': {'object_name': 'MacroDay'},
            'calories': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'carbs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'day': ('django.db.models.fields.DateField', [], {}),
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
            'url_slug': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'video_html': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
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
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'US/Pacific'", 'max_length': '40'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'base.traineralert': {
            'Meta': {'object_name': 'TrainerAlert'},
            'alert_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {}),
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