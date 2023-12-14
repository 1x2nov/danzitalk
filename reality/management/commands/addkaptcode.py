import urllib.parse as par
import urllib.request as req
import xml.etree.ElementTree
from django.core.management.base import BaseCommand
from reality.models import Reality
import time
import asyncio

class Command(BaseCommand):

    help = "Add danzi data"

    def handle(self, *args, **kwargs):

        start = time.time()

        Reality.objects.all().delete()

        loop.run_until_complete(main())
        loop.close()
        
        print("Working time :", time.time() - start)

loop = asyncio.get_event_loop()

async def main():
    url = 'http://apis.data.go.kr/1613000/AptListService2/getSidoAptList?'
    serviceKey = 'vDp95sBtTaP3d1x5+mrWmtHmvxzYVS4ni+bIpYXsbnNSpKsUmkUWNPEerkcKYXtVrUwmHTW5Nm0serBgCC1Shg=='
    params = {'serviceKey' : serviceKey, 
        'pageNo' : '1', 
        'numOfRows' : '20000',
        'sidoCode': '11',
    }

    param = par.urlencode(params)
    url = url + param
    data = req.urlopen(url).read()

    decode = data.decode("utf-8")
    trees = xml.etree.ElementTree.fromstring(decode)
    index = 1

    futures = []
    for tree in trees[1][0]:
        futures.append(asyncio.ensure_future(addKaptCode(tree, index)))
        await asyncio.sleep(0.01)
        index += 1

    await asyncio.gather(*futures)

async def addKaptCode(tree, index):
    kaptCode = tree.find("kaptCode").text
    l = [tree.find("as"+str(i)).text for i in range(1, 5) if tree.find("as"+str(i)) is not None]

    await loop.run_in_executor(None, lambda : Reality.objects.create(id=index, kaptCode=kaptCode, secondName=l[-1]))
    print(index,":",kaptCode)