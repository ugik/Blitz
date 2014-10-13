# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lift'
        db.create_table(u'workouts_lift', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('weight_or_body', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_weight_or_body', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lift_type', self.gf('django.db.models.fields.CharField')(default='R', max_length=1)),
        ))
        db.send_create_signal(u'workouts', ['Lift'])

        # Adding model 'Workout'
        db.create_table(u'workouts_workout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sets_grouped', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
        ))
        db.send_create_signal(u'workouts', ['Workout'])

        # Adding model 'Exercise'
        db.create_table(u'workouts_exercise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lift', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Lift'])),
            ('workout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Workout'])),
            ('sets_display', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'workouts', ['Exercise'])

        # Adding model 'ExerciseCustom'
        db.create_table(u'workouts_exercisecustom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Client'])),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Exercise'])),
            ('lift', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Lift'])),
            ('sets_display', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'workouts', ['ExerciseCustom'])

        # Adding model 'WorkoutSet'
        db.create_table(u'workouts_workoutset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lift', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Lift'])),
            ('workout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Workout'])),
            ('num_reps', self.gf('django.db.models.fields.IntegerField')()),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Exercise'], null=True)),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'workouts', ['WorkoutSet'])

        # Adding model 'WorkoutSetCustom'
        db.create_table(u'workouts_workoutsetcustom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Client'])),
            ('workoutset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.WorkoutSet'])),
            ('lift', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Lift'])),
            ('num_reps', self.gf('django.db.models.fields.IntegerField')()),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'workouts', ['WorkoutSetCustom'])

        # Adding model 'WorkoutPlan'
        db.create_table(u'workouts_workoutplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('trainer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Trainer'], null=True)),
        ))
        db.send_create_signal(u'workouts', ['WorkoutPlan'])

        # Adding model 'WorkoutPlanWeek'
        db.create_table(u'workouts_workoutplanweek', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workout_plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.WorkoutPlan'])),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'workouts', ['WorkoutPlanWeek'])

        # Adding model 'WorkoutPlanDay'
        db.create_table(u'workouts_workoutplanday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workout_plan_week', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.WorkoutPlanWeek'])),
            ('day_of_week', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('day_index', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('workout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Workout'])),
        ))
        db.send_create_signal(u'workouts', ['WorkoutPlanDay'])


    def backwards(self, orm):
        # Deleting model 'Lift'
        db.delete_table(u'workouts_lift')

        # Deleting model 'Workout'
        db.delete_table(u'workouts_workout')

        # Deleting model 'Exercise'
        db.delete_table(u'workouts_exercise')

        # Deleting model 'ExerciseCustom'
        db.delete_table(u'workouts_exercisecustom')

        # Deleting model 'WorkoutSet'
        db.delete_table(u'workouts_workoutset')

        # Deleting model 'WorkoutSetCustom'
        db.delete_table(u'workouts_workoutsetcustom')

        # Deleting model 'WorkoutPlan'
        db.delete_table(u'workouts_workoutplan')

        # Deleting model 'WorkoutPlanWeek'
        db.delete_table(u'workouts_workoutplanweek')

        # Deleting model 'WorkoutPlanDay'
        db.delete_table(u'workouts_workoutplanday')


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
        u'workouts.exercisecustom': {
            'Meta': {'object_name': 'ExerciseCustom'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Exercise']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Lift']"}),
            'sets_display': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
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
        },
        u'workouts.workoutsetcustom': {
            'Meta': {'object_name': 'WorkoutSetCustom'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Client']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Lift']"}),
            'num_reps': ('django.db.models.fields.IntegerField', [], {}),
            'workoutset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.WorkoutSet']"})
        }
    }

    complete_apps = ['workouts']