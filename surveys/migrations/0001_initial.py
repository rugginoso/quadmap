# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Anagraphics'
        db.create_table('surveys_anagraphics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('surveys', ['Anagraphics'])

        # Adding model 'Operator'
        db.create_table('surveys_operator', (
            ('anagraphics_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['surveys.Anagraphics'], unique=True, primary_key=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postal_address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('surveys', ['Operator'])

        # Adding model 'Area'
        db.create_table('surveys_area', (
            ('anagraphics_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['surveys.Anagraphics'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('surveys', ['Area'])

        # Adding model 'Survey'
        db.create_table('surveys_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('surveys', ['Survey'])

        # Adding model 'Question'
        db.create_table('surveys_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Survey'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('surveys', ['Question'])

        # Adding model 'Choice'
        db.create_table('surveys_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Question'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('surveys', ['Choice'])

        # Adding model 'Answer'
        db.create_table('surveys_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('anagraphics', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Anagraphics'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Question'])),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Choice'])),
            ('open_choice_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('surveys', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'Anagraphics'
        db.delete_table('surveys_anagraphics')

        # Deleting model 'Operator'
        db.delete_table('surveys_operator')

        # Deleting model 'Area'
        db.delete_table('surveys_area')

        # Deleting model 'Survey'
        db.delete_table('surveys_survey')

        # Deleting model 'Question'
        db.delete_table('surveys_question')

        # Deleting model 'Choice'
        db.delete_table('surveys_choice')

        # Deleting model 'Answer'
        db.delete_table('surveys_answer')


    models = {
        'surveys.anagraphics': {
            'Meta': {'object_name': 'Anagraphics'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'surveys.answer': {
            'Meta': {'object_name': 'Answer'},
            'anagraphics': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Anagraphics']"}),
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Choice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_choice_text': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Question']"})
        },
        'surveys.area': {
            'Meta': {'object_name': 'Area', '_ormbases': ['surveys.Anagraphics']},
            'anagraphics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['surveys.Anagraphics']", 'unique': 'True', 'primary_key': 'True'})
        },
        'surveys.choice': {
            'Meta': {'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'surveys.operator': {
            'Meta': {'object_name': 'Operator', '_ormbases': ['surveys.Anagraphics']},
            'anagraphics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['surveys.Anagraphics']", 'unique': 'True', 'primary_key': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postal_address': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'surveys.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Survey']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'surveys.survey': {
            'Meta': {'object_name': 'Survey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['surveys']