from django.contrib import admin
from django.db.models.loading import get_models
for m in get_models():
    exec "from %s import %s" % (m.__module__, m.__name__)

class ChoicesInline(admin.TabularInline):
	model = QuestionChoice
	extra = 0

class VarsInline(admin.TabularInline):
	model = QuestionVariable
	extra = 0


class QuestionChoiceAdmin(admin.ModelAdmin):
	add_form_template = 'question/admin/change_form.html'

class QuestionAdmin(admin.ModelAdmin):
	add_form_template = 'question/admin/change_form.html'
	change_form_template = 'question/admin/change_form.html'
	inlines = [VarsInline, ChoicesInline]

class ExposInline(admin.StackedInline):
    model = Exposition
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ExposInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Exposition)
admin.site.register(Submission)
admin.site.register(Vote)
admin.site.register(VoteCategory)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice, QuestionChoiceAdmin)