from django.db import models
from fields import CountryField

class Anagraphics(models.Model):
	name = models.CharField(max_length=255)
	country = CountryField()

	class Meta:
		verbose_name = "registry"
		verbose_name_plural = "registries"

class Operator(Anagraphics):
	organization = models.CharField(max_length=255)
	department = models.CharField(max_length=255)
	position = models.CharField(max_length=255)
	phone = models.CharField(max_length=255)
	postal_address = models.CharField(max_length=255)
	email = models.EmailField()

	class Meta:
		verbose_name = "Stakeholder"

	def __unicode__(self):
		return "%s - %s: %s" % (self.country, self.organization, self.name)

	@models.permalink
	def get_absolute_url(self):
		return ('edit_operator', [str(self.id)])


class Area(Anagraphics):
	# geographics inidcation
	# numeric values

	def __unicode__(self):
		return "%s - %s" % (self.country, self.name)

	@models.permalink
	def get_absolute_url(self):
		return ('edit_area', [str(self.id)])

class Survey(models.Model):
	SURVEY_TYPES = (
		('O', 'stakeholder'),
		('R', 'remote'),
		('L', 'local'),
	)
	title = models.CharField(max_length=30)
	type = models.CharField(max_length=1, choices=SURVEY_TYPES)

	def __unicode__(self):
		return "%s (%s)" % (self.title, self.get_type_display())


class Question(models.Model):
	survey = models.ForeignKey(Survey)
	text = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order']

	def __unicode__(self):
		return "%s: %s" % (self.survey.title, self.text)

	def is_full_open(self):
		# if the question has only one choice and is open
		return len(self.choice_set.all()) == 1 and self.choice_set.all()[0].type == 'O'

class Choice(models.Model):
	CHOICE_TYPES = (
		('C', 'Close'),
		('O', 'Open')
	)
	question = models.ForeignKey(Question)
	text = models.CharField(max_length=255)
	type = models.CharField(max_length=1, choices=CHOICE_TYPES)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order']

	def __unicode__(self):
		return self.text


class AnswerManager(models.Manager):
	def get_all_operator_answers_for_question(self, question):
		return super(AnswerManager, self).get_query_set().filter(question=question)

	def get_all_user_answers_for_question(self, question, zone=None, age=None, gender=None):
		q = super(AnswerManager, self).get_query_set().filter(question=question)
		if zone:
			q = q.filter(zone=zone)
		if age:
			q = q.filter(age=age)
		if gender:
			q = q.filter(gender=gender)
		return q


class Answer(models.Model):
	anagraphics = models.ForeignKey(Anagraphics)
	question = models.ForeignKey(Question)
	choice = models.ForeignKey(Choice)
	open_choice_text = models.TextField()

	objects = AnswerManager()
