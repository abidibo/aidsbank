# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Centre'
        db.create_table(u'aidsbank_centre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timetable', self.gf('ckeditor.fields.RichTextField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'aidsbank', ['Centre'])

        # Adding model 'Manager'
        db.create_table(u'aidsbank_manager', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'aidsbank', ['Manager'])

        # Adding M2M table for field centres on 'Manager'
        m2m_table_name = db.shorten_name(u'aidsbank_manager_centres')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('manager', models.ForeignKey(orm[u'aidsbank.manager'], null=False)),
            ('centre', models.ForeignKey(orm[u'aidsbank.centre'], null=False))
        ))
        db.create_unique(m2m_table_name, ['manager_id', 'centre_id'])

        # Adding model 'Applicant'
        db.create_table(u'aidsbank_applicant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('cap', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'aidsbank', ['Applicant'])

        # Adding model 'AidType'
        db.create_table(u'aidsbank_aidtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'aidsbank', ['AidType'])

        # Adding model 'Aid'
        db.create_table(u'aidsbank_aid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.AidType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('ckeditor.fields.RichTextField')()),
            ('card', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('deposit', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('max_loan_duration', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'aidsbank', ['Aid'])

        # Adding model 'Asset'
        db.create_table(u'aidsbank_asset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.Aid'])),
            ('centre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.Centre'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('condition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('laon', self.gf('django.db.models.fields.BooleanField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'aidsbank', ['Asset'])

        # Adding model 'Loan'
        db.create_table(u'aidsbank_loan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.Asset'])),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.Applicant'])),
            ('addressee', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('deposit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('reservation_date', self.gf('django.db.models.fields.DateField')()),
            ('loan_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('loan_duration', self.gf('django.db.models.fields.IntegerField')(max_length=8, null=True, blank=True)),
            ('renewal_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('return_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('solicit_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('follow_up', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'aidsbank', ['Loan'])

        # Adding model 'Movement'
        db.create_table(u'aidsbank_movement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.Asset'])),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.Manager'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('loan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aidsbank.Loan'], null=True, blank=True)),
            ('last_status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'aidsbank', ['Movement'])


    def backwards(self, orm):
        # Deleting model 'Centre'
        db.delete_table(u'aidsbank_centre')

        # Deleting model 'Manager'
        db.delete_table(u'aidsbank_manager')

        # Removing M2M table for field centres on 'Manager'
        db.delete_table(db.shorten_name(u'aidsbank_manager_centres'))

        # Deleting model 'Applicant'
        db.delete_table(u'aidsbank_applicant')

        # Deleting model 'AidType'
        db.delete_table(u'aidsbank_aidtype')

        # Deleting model 'Aid'
        db.delete_table(u'aidsbank_aid')

        # Deleting model 'Asset'
        db.delete_table(u'aidsbank_asset')

        # Deleting model 'Loan'
        db.delete_table(u'aidsbank_loan')

        # Deleting model 'Movement'
        db.delete_table(u'aidsbank_movement')


    models = {
        u'aidsbank.aid': {
            'Meta': {'object_name': 'Aid'},
            'card': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deposit': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'description': ('ckeditor.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_loan_duration': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.AidType']"})
        },
        u'aidsbank.aidtype': {
            'Meta': {'object_name': 'AidType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'aidsbank.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'cap': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'aidsbank.asset': {
            'Meta': {'object_name': 'Asset'},
            'aid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.Aid']"}),
            'centre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.Centre']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'laon': ('django.db.models.fields.BooleanField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'aidsbank.centre': {
            'Meta': {'object_name': 'Centre'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timetable': ('ckeditor.fields.RichTextField', [], {})
        },
        u'aidsbank.loan': {
            'Meta': {'object_name': 'Loan'},
            'addressee': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.Applicant']"}),
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.Asset']"}),
            'deposit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'follow_up': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loan_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'loan_duration': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'renewal_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'reservation_date': ('django.db.models.fields.DateField', [], {}),
            'return_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'solicit_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'aidsbank.manager': {
            'Meta': {'object_name': 'Manager'},
            'centres': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['aidsbank.Centre']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'aidsbank.movement': {
            'Meta': {'object_name': 'Movement'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.Asset']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.Loan']", 'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aidsbank.Manager']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['aidsbank']