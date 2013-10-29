# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.leading_answer'
        db.add_column(u'show_question', 'leading_answer',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='next_question', null=True, to=orm['show.Answer']),
                      keep_default=False)

        # Deleting field 'Answer.next_question'
        db.delete_column(u'show_answer', 'next_question_id')


    def backwards(self, orm):
        # Deleting field 'Question.leading_answer'
        db.delete_column(u'show_question', 'leading_answer_id')

        # Adding field 'Answer.next_question'
        db.add_column(u'show_answer', 'next_question',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='pre_answer', null=True, to=orm['show.Question'], blank=True),
                      keep_default=False)


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
            'modifier': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'possible_answers'", 'to': u"orm['show.Question']"}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': u"orm['show.Scale']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'show.location': {
            'Meta': {'object_name': 'Location'},
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'directions': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'safe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': u"orm['show.Scale']"}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'show.note': {
            'Meta': {'object_name': 'Note'},
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes'", 'to': u"orm['show.Profile']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'show.profile': {
            'Meta': {'object_name': 'Profile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'answered_questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['show.Question']", 'symmetrical': 'False'}),
            'birth': ('django.db.models.fields.DateField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'force_questions': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'given_answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['show.Answer']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'to': u"orm['show.Location']"}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'visitors'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['show.Location']"}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': u"orm['show.Question']"}),
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['show.Scale']", 'through': u"orm['show.Rating']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Profiles'", 'to': u"orm['auth.User']"})
        },
        u'show.question': {
            'Meta': {'object_name': 'Question'},
            'can_start': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leading_answer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next_question'", 'null': 'True', 'to': u"orm['show.Answer']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'show.rating': {
            'Meta': {'object_name': 'Rating'},
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