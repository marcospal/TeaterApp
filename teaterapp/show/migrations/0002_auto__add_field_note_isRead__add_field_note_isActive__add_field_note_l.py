# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Note.isRead'
        db.add_column(u'show_note', 'isRead',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Note.isActive'
        db.add_column(u'show_note', 'isActive',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Note.location'
        db.add_column(u'show_note', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='notes', null=True, to=orm['show.Location']),
                      keep_default=False)


        # Changing field 'Note.profile'
        db.alter_column(u'show_note', 'profile_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['show.Profile']))

    def backwards(self, orm):
        # Deleting field 'Note.isRead'
        db.delete_column(u'show_note', 'isRead')

        # Deleting field 'Note.isActive'
        db.delete_column(u'show_note', 'isActive')

        # Deleting field 'Note.location'
        db.delete_column(u'show_note', 'location_id')


        # Changing field 'Note.profile'
        db.alter_column(u'show_note', 'profile_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['show.Profile']))

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'show.answer': {
            'Meta': {'object_name': 'Answer'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignoreLocations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['show.Location']", 'null': 'True', 'blank': 'True'}),
            'modifier': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'possible_answers'", 'to': u"orm['show.Question']"}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': u"orm['show.Scale']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'show.color': {
            'Meta': {'object_name': 'Color'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'ffffff'", 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'show.location': {
            'Meta': {'object_name': 'Location'},
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'capacity_min': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'directions': ('django.db.models.fields.TextField', [], {'max_length': '256', 'blank': 'True'}),
            'first_arrived_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isEnding': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isStartRoom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parameters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['show.Scale']", 'through': u"orm['show.Parameter']", 'symmetrical': 'False'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'safe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': u"orm['show.Scale']"}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'show.note': {
            'Meta': {'object_name': 'Note'},
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'isRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notes'", 'null': 'True', 'to': u"orm['show.Location']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notes'", 'null': 'True', 'to': u"orm['show.Profile']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '256'})
        },
        u'show.parameter': {
            'Meta': {'unique_together': "(('location', 'scale'),)", 'object_name': 'Parameter'},
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['show.Location']"}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['show.Scale']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        u'show.profile': {
            'Meta': {'object_name': 'Profile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'answered_questions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'profiles_that_have_answered'", 'symmetrical': 'False', 'through': u"orm['show.QuestionCount']", 'to': u"orm['show.Question']"}),
            'available_locations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'posible_profiles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['show.Location']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'force_questions': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'given_answers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'profiles_that_have_answered'", 'blank': 'True', 'to': u"orm['show.Answer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'to': u"orm['show.Location']"}),
            'location_set_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pending_profiles'", 'null': 'True', 'to': u"orm['show.Question']"}),
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['show.Scale']", 'through': u"orm['show.Rating']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Profiles'", 'to': u"orm['auth.User']"}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'show.question': {
            'Meta': {'object_name': 'Question'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leading_answer': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'next_question'", 'unique': 'True', 'null': 'True', 'to': u"orm['show.Answer']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'show.questioncount': {
            'Meta': {'object_name': 'QuestionCount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['show.Profile']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['show.Question']"}),
            'times': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'show.rating': {
            'Meta': {'unique_together': "(('profile', 'scale'),)", 'object_name': 'Rating'},
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['show.Profile']"}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['show.Scale']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        u'show.scale': {
            'Meta': {'object_name': 'Scale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['show']