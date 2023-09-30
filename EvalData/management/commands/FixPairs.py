from django.core.management.base import BaseCommand
from EvalData.models import *
from Campaign.models import *

l = [[397, 'euskadi.eu'], [347, 'cmbacktrans.eu'], [74, 'kurt.mt'], [142, 'kurt.mt'], [300, 'kurt.mt'], [177, 'cmbacktrans.eu'], [364, 'nllb.mt'], [178, 'euskadi.eu'], [294, 'cmbacktrans.eu'], [60, 'kurt.mt'], [318, 'nllb.mt'], [284, 'kurt.mt'], [152, 'gtrans.mt'], [17, 'kurt.mt'], [234, 'kurt.mt'], [234, 'gtrans.mt'], [212, 'gtrans.mt'], [215, 'kurt.mt'], [224, 'nllb.mt'], [344, 'kurt.mt'], [97, 'gtrans.mt'], [9, 'nllb.eu'], [128, 'gtrans.mt'], [253, 'kurt.mt'], [163, 'nllb.mt'], [307, 'nllb.mt'], [400, 'euskadi.eu'], [260, 'nllb.mt']]

class Command(BaseCommand):
    def handle(self, *args, **options):

        pairs = TextPair.objects.all()

        for pair in pairs:
            if [pair.itemID, pair.targetID] in l:
                if not pair.completed:
                    print("updating", pair, "...")
                    pair.completed = True
                    pair.save()
