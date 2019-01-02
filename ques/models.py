# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models




class SRecord(models.Model):
    record_id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey('SUser', models.DO_NOTHING, db_column='user', blank=True, null=True)
    question = models.ForeignKey('TQuestion', models.DO_NOTHING, db_column='question', blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    option = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 's_record'


class SUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)
    category = models.ForeignKey('TCategory', models.DO_NOTHING, db_column='category', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 's_user'


class TAnswer(models.Model):
    answer_id = models.CharField(primary_key=True, max_length=255)
    option = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=15538, blank=True, null=True)
    question = models.ForeignKey('TQuestion', models.DO_NOTHING, db_column='question', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_answer'


class TCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    status = models.IntegerField()

    class Meta:
        managed = True
        db_table = 't_category'


class TChapter(models.Model):
    chapter_id = models.CharField(max_length=255,primary_key=True)
    category = models.IntegerField()
    chapter = models.IntegerField()
    title = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 't_chapter'


class TOption(models.Model):
    option_id = models.CharField(primary_key=True, max_length=255)
    question = models.ForeignKey('TQuestion', models.DO_NOTHING, db_column='question', blank=True, null=True)
    content = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_option'


class TQuestion(models.Model):
    question_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(TCategory, models.DO_NOTHING, db_column='category')
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    chapter = models.ForeignKey(TChapter, models.DO_NOTHING, db_column='chapter')
    number = models.IntegerField()
    type = models.IntegerField()
    create_time = models.CharField(max_length=255)
    status = models.IntegerField()
    owner = models.CharField(max_length=255)
    modify_time = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 't_question'
