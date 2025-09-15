from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Quiz)
admin.site.register(models.MultipleChoice)
admin.site.register(models.MultipleChoiceOptions)
admin.site.register(models.FillInBlank)
admin.site.register(models.FillInBlankSentence)
admin.site.register(models.Information)
admin.site.register(models.Attempt)
admin.site.register(models.MultipleChoiceResponse)
admin.site.register(models.FillInBlankReponse)
admin.site.register(models.FillInBlankAnswer)
