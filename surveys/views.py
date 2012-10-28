from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from surveys import models

def survey_compile(request, survey_id):
	survey = get_object_or_404(models.Survey, id=survey_id)

	anagraphics = []
	if survey.type == 'O':
		anagraphics = sorted(models.Operator.objects.all(), key=str)
	else:
		anagraphics = sorted(models.Area.objects.all(), key=str)

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

		return HttpResponseRedirect(reverse('index'))

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

def csv_export(request):
	HIDDEN_FIELDS = (
		'order',
		'anagraphics_ptr',
	)

	NAME_MAP = {
		'anagraphics': 'registry'
	}

	import zipfile
	from datetime import datetime
	import StringIO
	from django.db.models.fields.related import ForeignKey

	response = HttpResponse(mimetype='applicaiton/zip')
	response['Content-Disposition'] = 'filename=quadmap-export-%s.zip' % datetime.now().isoformat()

	buffer = StringIO.StringIO()
	zip = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)

	files = {
		'stakeholders.csv': models.Operator,
		'areas.csv': models.Area,
		'surveys.csv': models.Survey,
		'questions.csv': models.Question,
		'choices.csv': models.Choice,
		'answers.csv': models.Answer,
	}

	for n,c in files.items():
		fields = c._meta.fields
		lines = []
		titles = [field.name for field in fields if field.name not in HIDDEN_FIELDS]

		for index, title in enumerate(titles):
			if title in NAME_MAP.keys():
				titles[index] = NAME_MAP[title]

		lines.append(";".join(titles))

		for obj in c.objects.all():
			values = []
			for field in fields:
				if field.name in HIDDEN_FIELDS:
					continue
				if isinstance(field, ForeignKey):
					values.append(str(getattr(obj, field.name).id))
				else:
					values.append(str(getattr(obj, field.name)))
			lines.append(';'.join(values))

		zip.writestr(n, '\n'.join(lines))

	zip.close()
	buffer.flush()

	data = buffer.getvalue()
	buffer.close()

	response.write(data)

	return response
