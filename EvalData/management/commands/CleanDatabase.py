from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from EvalData.models import *
from Campaign.models import *

from random import choice

class Command(BaseCommand):
    def handle(self, *args, **options):

        del args
        del options

        print("Script deactivated because there is prod data in the database.")

        # random_letter = choice(list("abcdefghijklmnopqrstuvwxyz"))

        # prompt = f"""
        # Are you sure, 100% sure, fully sure, that you wish to delete EVERYTHING in your database?
        # If so, type the letter '{random_letter}': 
        # """
        # res = input(prompt)

        # if res == random_letter:

        #     for model in [
        #         DirectAssessmentResult,
        #         TextPair,
        #         DirectAssessmentTask,
        #         CampaignData, # Batch 
        #         Metadata,
        #         Market,
        #         Campaign,
        #     ]:
        #         print(f"Deleting all instances of {model}...")
        #         model.objects.filter().delete()

        # else:
        #     print("Nevermind!")