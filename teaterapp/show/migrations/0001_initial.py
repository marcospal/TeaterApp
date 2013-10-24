# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Scale'
        db.create_table(u'show_scale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'show', ['Scale'])

        # Adding model 'Question'
        db.create_table(u'show_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('can_start', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'show', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'show_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='possible_answers', to=orm['show.Question'])),
            ('next_question', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pre_answer', null=True, to=orm['show.Question'])),
            ('scale', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='answers', null=True, to=orm['show.Scale'])),
            ('modifier', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'show', ['Answer'])

        # Adding model 'Location'
        db.create_table(u'show_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('directions', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('safe', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('scale', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='locations', null=True, to=orm['show.Scale'])),
        ))
        db.send_create_signal(u'show', ['Location'])

        # Adding model 'Profile'
        db.create_table(u'show_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Profiles', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('force_questions', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='answers', null=True, to=orm['show.Question'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('year_of_birth', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profiles', null=True, to=orm['show.Location'])),
        ))
        db.send_create_signal(u'show', ['Profile'])

        # Adding M2M table for field answered_questions on 'Profile'
        m2m_table_name = db.shorten_name(u'show_profile_answered_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'show.profile'], null=False)),
            ('question', models.ForeignKey(orm[u'show.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'question_id'])

        # Adding M2M table for field given_answers on 'Profile'
        m2m_table_name = db.shorten_name(u'show_profile_given_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'show.profile'], null=False)),
            ('answer', models.ForeignKey(orm[u'show.answer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'answer_id'])

        # Adding M2M table for field locations on 'Profile'
        m2m_table_name = db.shorten_name(u'show_profile_locations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'show.profile'], null=False)),
            ('location', models.ForeignKey(orm[u'show.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'location_id'])

        # Adding model 'Rating'
        db.create_table(u'show_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('changed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['show.Profile'])),
            ('scale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['show.Scale'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal(u'show', ['Rating'])

        # Adding model 'Note'
        db.create_table(u'show_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('changed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notes', to=orm['show.Profile'])),
        ))
        db.send_create_signal(u'show', ['Note'])


    def backwards(self, orm):
        # Deleting model 'Scale'
        db.delete_table(u'show_scale')

        # Deleting model 'Question'
        db.delete_table(u'show_question')

        # Deleting model 'Answer'
        db.delete_table(u'show_answer')

        # Deleting model 'Location'
        db.delete_table(u'show_location')

        # Deleting model 'Profile'
        db.delete_table(u'show_profile')

        # Removing M2M table for field answered_questions on 'Profile'
        db.delete_table(db.shorten_name(u'show_profile_answered_questions'))

        # Removing M2M table for field given_answers on 'Profile'
        db.delete_table(db.shorten_name(u'show_profile_given_answers'))

        # Removing M2M table for field locations on 'Profile'
        db.delete_table(db.shorten_name(u'show_profile_locations'))

        # Deleting model 'Rating'
        db.delete_table(u'show_rating')

        # Deleting model 'Note'
        db.delete_table(u'show_note')


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
            'next_question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pre_answer'", 'null': 'True', 'to': u"orm['show.Question']"}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Profiles'", 'to': u"orm['auth.User']"}),
            'year_of_birth': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'show.question': {
            'Meta': {'object_name': 'Question'},
            'can_start': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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