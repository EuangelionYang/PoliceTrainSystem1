from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Training)
admin.site.register(TrainingToLearner)
admin.site.register(Chapter)