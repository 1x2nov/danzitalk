from django.core.management.base import BaseCommand
import time
import itertools
from reality.models import Reality

bjdCodeSet = set(reality.bjdCode[:5] for reality in Reality.objects.all())

class Command(BaseCommand):

    help = "Update building register in danzi (reality model) data"

    def handle(self, *args, **kwargs):

        start = time.time()

        productSet = set(itertools.product(range(2018, 2022+1), range(1, 12+1), bjdCodeSet))
        print(len(list(productSet)))

        print(time.localtime().tm_year, time.localtime().tm_mon)

        print("Working time :", time.time() - start)