from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from surveys.models import *


def add_link_field(target_model = None, field = '', link_text = unicode):
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()
        def link(self, instance):
            app_name = instance._meta.app_label
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            link_obj = getattr(instance, field, None) or instance
            url = reverse(reverse_path, args = (link_obj.id,))
            return mark_safe("<a href='%s'>%s</a>" % (url, link_text(link_obj)))
        link.allow_tags = True
        link.short_description = reverse_name + ' link'
        cls.link = link
        cls.readonly_fields = list(getattr(cls, 'readonly_fields', [])) + ['link']
        return cls
    return add_link

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
    sortable_field_name = 'order'

@add_link_field()
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    sortable_field_name = 'order'

@add_link_field('survey', 'survey')
class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)

class SurveyAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Operator)
admin.site.register(Area)
