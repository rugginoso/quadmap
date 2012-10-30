from django import forms

class ReportByNameForm(forms.Form):
	name = forms.CharField(max_length=255)

class ReportByQuestionForm(forms.Form):
	text = forms.CharField(max_length=255)
