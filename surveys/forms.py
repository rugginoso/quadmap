from django.forms.models import modelformset_factory, inlineformset_factory, BaseInlineFormSet, ModelForm
from django.forms.formsets import DELETION_FIELD_NAME
from surveys import models

class OperatorForm(ModelForm):
    class Meta:
        model = models.Operator

class SurveyForm(ModelForm):
	class Meta:
		model = models.Survey

# http://yergler.net/blog/2009/09/27/nested-formsets-with-django/

ChoiceFormSet = inlineformset_factory(models.Question,
									  models.Choice,
									  extra=1)

class BaseQuestionFormSet(BaseInlineFormSet):
	def add_fields(self, form, index):
		super(BaseQuestionFormSet, self).add_fields(form, index)

		try:
			instance = self.get_queryset()[index]
			pk_value = instance.pk
		except IndexError:
			instance = None
			pk_value = hash(form.prefix)

		form.nested = [
			ChoiceFormSet(instance=instance,
						  prefix='choices_%s' % pk_value)
		]

	def is_valid(self):
		result = super(BaseQuestionFormSet, self).is_valid()

		for form in self.forms:
			if hasattr(form, 'nested'):
				for n in form.nested:
					n.data = form.data
					if form.is_bound:
						n.is_bound = True
					for nform in n:
						nform.data = form.data
						if form.is_bound:
							nform.is_bound = True
					result = result and n.is_valid()

		return result

	def should_delete(self, form):
		if self.can_delete:
			raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
			return form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)

		return False

	def save_new(self, form, commit=True):
		instance = super(BaseQuestionFormSet, self).save_new(form, commit=commit)

		form.instance = instance

		for n in form.nested:
			n.instance = instance

			for cd in n.cleaned_data:
				cd[n.fk.name] = instance

		return instance

	def save_all(self, commit=True):
		objects = self.save(commit=False)

		if commit:
			for o in objects:
				o.save()

		if not commit:
			self.save_m2m()

		for form in set(self.initial_forms + self.saved_forms):
			if self.should_delete(form): continue

			for n in form.nested:
				n.save(commit=commit)

QuestionFormSet = inlineformset_factory(models.Survey,
										models.Question,
										formset=BaseQuestionFormSet,
										extra=1)
