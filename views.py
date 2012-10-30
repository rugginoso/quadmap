from django.shortcuts import render_to_response
from surveys.models import Survey, Operator, Area

def index(request):
	title = 'Index'
	surveys = Survey.objects.all()

	return render_to_response('index.html', locals())
