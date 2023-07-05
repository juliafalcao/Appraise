from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from EvalData.models import *
from Campaign.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):

        del args
        del options

        prompt = "Are you sure, 100% sure, fully sure, that you wish to delete EVERYTHING in the database? (y/n) "
        res = input(prompt)

        if res == "y":

            for model in [
                DirectAssessmentResult,
                TextPair,
                DirectAssessmentTask,
                CampaignData, # Batch 
                Metadata,
                Market,
                Campaign,
            ]:
                print(f"Deleting all instances of {model}...")
                model.objects.filter().delete()
