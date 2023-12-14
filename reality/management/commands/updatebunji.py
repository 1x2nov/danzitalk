from django.core.management.base import BaseCommand
from reality.models import Reality
import time
import re

class Command(BaseCommand):

    help = "Add address in danzi (reality model) data"

    def handle(self, *args, **kwargs):
        start = time.time()
        Reality.objects.all().update(bun=None, ji=None)

        for reality in Reality.objects.all():

            print("[ Reality id : "+str(reality.id)+" ]")
            print('- Address :',reality.kaptAddr)
            regax = re.search(r'\s(\d+[-]*\d*)\s', reality.kaptAddr)
            
            if regax is not None:
                l = regax[1].split("-")
                bun = l[0]
                ji = l[1] if len(l) > 1 else 0

                print("번:", bun)
                print("지:", ji)

                Reality.objects.filter(id=reality.id).update(bun=bun,ji=ji)

        print("Working time :", time.time() - start)