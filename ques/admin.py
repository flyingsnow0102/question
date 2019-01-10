from django.contrib import admin

from ques.models import SRecord, SUser, TQuestion, TChapter, TCategory, TOption, TAnswer


# Register your models here.
class Question(admin.ModelAdmin):
    list_display = ('title', 'category_title', 'chapter_title', 'create_time')
    search_fields = ('title', 'category__title', 'chapter__title')

    def chapter_title(self, obj):
        return obj.chapter.title

    def category_title(self, obj):
        return obj.category.title


class Option(admin.ModelAdmin):
    list_display = ('question_title', 'content')
    search_fields = ('question__title', 'content')

    def question_title(self, obj):
        return obj.question.title


class Answer(admin.ModelAdmin):
    list_display = ('question_title', 'option')
    search_fields = ('question__title', 'option')

    def question_title(self, obj):
        return obj.question.title


admin.site.register(SRecord)
admin.site.register(SUser)
admin.site.register(TQuestion, Question)
admin.site.register(TOption, Option)
admin.site.register(TAnswer, Answer)
admin.site.register([TCategory, TChapter])
