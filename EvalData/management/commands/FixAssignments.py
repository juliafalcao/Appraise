from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from EvalData.models import *
from Campaign.models import *

import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):

        tasks = DirectAssessmentTask.objects.all()
        # tasks = DirectAssessmentTask.objects.filter()

        for task in tasks:
            print(task, task.assignedTo.all())

            # print("clearing", task, "...")
            # task.assignedTo.clear()
