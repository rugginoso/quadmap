from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from surveys import models
from surveys import forms

def survey_index(request):
	surveys = models.Survey.objects.all()

	return render_to_response('surveys/survey_list.html', {'title': 'Surveys index',
													'surveys': surveys})

def survey_new(request):
	if request.method == 'POST':
		survey_form = forms.SurveyForm(request.POST)
		if survey_form.is_valid():
			survey = survey_form.save(commit=False)
			question_formset = forms.QuestionFormSet(request.POST, instance=survey)
			if question_formset.is_valid():
				survey.save()
				question_formset.save_all()
				return HttpResponseRedirect(reverse(survey_edit, args=(survey.id,)))
	else:
		survey_form = forms.SurveyForm()
		question_formset = forms.QuestionFormSet()

	return render_to_response('surveys/survey_edit.html',
							 {'title': 'New survey',
							  'survey_form': survey_form,
							  'question_formset': question_formset},
							  context_instance=RequestContext(request))


def survey_edit(request, survey_id):
	survey = get_object_or_404(models.Survey, id=survey_id)

	if request.method == 'POST':
		survey_form = forms.SurveyForm(request.POST, instance=survey)
		if survey_form.is_valid():
			survey = survey_form.save(commit=False)
			question_formset = forms.QuestionFormSet(request.POST, instance=survey)
			if question_formset.is_valid():
				survey.save()
				question_formset.save_all()

	survey_form = forms.SurveyForm(instance=survey)
	question_formset = forms.QuestionFormSet(instance=survey)

	return render_to_response('surveys/survey_edit.html',
							 {'title': 'Edit survey',
							  'survey_form': survey_form,
							  'question_formset': question_formset},
							  context_instance=RequestContext(request))

def survey_delete(request, survey_id):
	survey = get_object_or_404(models.Survey, id=survey_id)
	survey.delete()

	return HttpResponseRedirect(reverse('index'))

def survey_compile(request, survey_id):
	survey = get_object_or_404(models.Survey, id=survey_id)

	anagraphics = []
	if survey.type == 'O':
		anagraphics = models.Operator.objects.all()
	else:
		anagraphics = models.Area.objects.all()

	if request.method == 'POST':
		anagraphic = get_object_or_404(models.Anagraphics, id=int(request.POST.get('anagraphics', 0)))

		for data in request.POST:
			question_data = data.split('_')
			if len(question_data) != 2: continue
			if question_data[0] != 'question': continue

			choice_id = int(request.POST.get(data, 0))

			question = get_object_or_404(models.Question, id=int(question_data[1]))
			choice = get_object_or_404(models.Choice, id=choice_id)

			choice_text = ""
			if choice.type == 'O':
				choice_text = request.POST.get('choice_text_%d' % choice_id, "")

			models.Answer(anagraphics=anagraphic,
						  question=question,
						  choice=choice,
						  open_choice_text=choice_text).save()

		return HttpResponseRedirect(reverse(survey_index))

	return render_to_response('surveys/survey_compile.html',
							  {'title': 'Compile survey',
							   'survey': survey,
							   'anagraphics': anagraphics},
							   context_instance=RequestContext(request))

def survey_report(request, survey_id):
	survey = get_object_or_404(models.Survey, id=survey_id)

	answers = models.Answer.objects.filter(question__survey=survey)

	return render_to_response('surveys/survey_report.html',
							  {'title': 'Survey report',
							   'answers': answers})
