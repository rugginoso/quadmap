from django.shortcuts import render_to_response
from quadmap.surveys.models import Survey, Operator, Area

def index(request):
	surveys = Survey.objects.all()
	operators = Operator.objects.all()
	areas = Area.objects.all()

	return render_to_response('index.html', locals())
