from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from EvalData.models import *
from Campaign.models import *

from random import choice
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):

        tasks = DirectAssessmentTask.objects.all()

        for task in tasks:
            print("task:", task)
            print("requiredAnnotations:", task.requiredAnnotations)

            if task.requiredAnnotations == 3:
                print(f"updating {task}...")
                task.requiredAnnotations = 1
                task.save()
