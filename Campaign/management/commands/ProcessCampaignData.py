from json import loads
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from Campaign.models import Campaign
from EvalData.models import DirectAssessmentTask

# pylint: disable=C0111,C0330,E1101
class Command(BaseCommand):
    help = 'Validates campaign data batches'

    def add_arguments(self, parser):
        parser.add_argument(
          'campaign_name', type=str,
          help='Name of the campaign you want to process data for'
        )
        # TODO: add argument to specify batch user

    def handle(self, *args, **options):
        campaign_name = options['campaign_name']

        # Identify Campaign instance for given name
        campaign = Campaign.objects.filter(campaignName=campaign_name).first()
        if not campaign:
            _msg = 'Failure to identify campaign {0}'.format(campaign_name)
            self.stdout.write(_msg)
            return

        # Identify batch user who needs to be a superuser
        batch_user = User.objects.filter(is_superuser=True).first()
        if not batch_user:
            _msg = 'Failure to identify batch user'
            self.stdout.write(_msg)
            return

        # TODO: add rollback in case of errors
        for batch_data in campaign.batches.filter(dataValid=True):            
            DirectAssessmentTask.import_from_json(
              campaign, batch_user, batch_data
            )
