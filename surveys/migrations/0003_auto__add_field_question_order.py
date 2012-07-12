# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.order'
        db.add_column('surveys_question', 'order',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.order'
        db.delete_column('surveys_question', 'order')


    models = {
        'surveys.anagraphics': {
            'Meta': {'object_name': 'Anagraphics'},
            'country': ('quadmap.surveys.fields.CountryField', [], {'max_length': '3'}),
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
            'Meta': {'ordering': "['order']", 'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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