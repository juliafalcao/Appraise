from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from EvalData.models import *
from Campaign.models import *

from random import choice
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):

        df_eval = pd.read_csv("/home/juliafalcao/thesis_data/es-eu/df_eval.csv")

        # query all TextPairs of type REF from the SpaEusV1 campaign
        textpairs = TextPair.objects.filter(itemType="REF", metadata_id=3)

        for pair in textpairs:
            print("pair:", pair)
            pair.retired = False
            pair.activated = True

            if pair.sourceText == pair.targetText:
                # pair.targetText = 
                row = df_eval[df_eval.itemId == pair.itemID].iloc[0]
                ref_text = row.ref

                pair.targetText = ref_text
                pair.save()

        # _str_name, activated, activatedBy, activatedBy_id, completed, completedBy, completedBy_id, createdBy, createdBy_id, dateActivated, dateCompleted, dateCreated, dateModified, dateRetired, evaldata_directassessmentresults, evaldata_directassessmenttasks, id, itemID, itemType, metadata, metadata_id, modifiedBy, modifiedBy_id, rawData, retired, retiredBy, retiredBy_id, sourceID, sourceText, targetID, targetText, textpairwithcontext, textpairwithdomain
